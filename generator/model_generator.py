"""Generate Pydantic models from parsed OCSF schema."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from generator.schema_types import (
    ParsedSchema,
    Requirement,
    SchemaAttribute,
    SchemaEnum,
)
from generator.utils import (
    make_valid_identifier,
    ocsf_type_to_python,
    snake_to_pascal,
)


@dataclass
class FieldInfo:
    """Processed field information for templates."""

    field_name: str
    type_annotation: str
    description: str
    is_required: bool
    requirement: str


class ModelGenerator:
    """Generate Pydantic models from OCSF schema."""

    def __init__(self, schema: ParsedSchema, output_dir: Path):
        self.schema = schema
        self.output_dir = output_dir
        # Handle both "v1.2.0" and "1.7.0" formats
        version_str = schema.version
        if not version_str.startswith("v"):
            version_str = f"v{version_str}"
        self.version_module = version_str.replace(".", "_")  # v1.7.0 -> v1_7_0

        # Set up Jinja2
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate_all(self) -> None:
        """Generate all models for the schema."""
        version_dir = self.output_dir / self.version_module

        # Create directories
        (version_dir / "enums").mkdir(parents=True, exist_ok=True)
        (version_dir / "objects").mkdir(parents=True, exist_ok=True)
        (version_dir / "events").mkdir(parents=True, exist_ok=True)

        # Generate enums
        enum_names = self._generate_enums(version_dir / "enums")

        # Generate objects
        object_names = self._generate_objects(version_dir / "objects")

        # Generate events
        event_names = self._generate_events(version_dir / "events")

        # Generate __init__.py files
        self._generate_init_files(version_dir, enum_names, object_names, event_names)

        print(
            f"Generated {len(enum_names)} enums, {len(object_names)} objects, {len(event_names)} events"
        )

    def _generate_enums(self, output_dir: Path) -> list[str]:
        """Generate enum files."""
        template = self.env.get_template("enum.py.jinja2")
        generated = []

        for name, enum in self.schema.enums.items():
            class_name = snake_to_pascal(name)

            # Clean up enum values - ensure valid Python identifiers
            clean_values = {}
            for value, member_name in enum.values.items():
                clean_name = make_valid_identifier(member_name).upper()
                clean_values[value] = clean_name

            enum_copy = SchemaEnum(
                name=enum.name,
                description=enum.description,
                values=clean_values,
                value_descriptions=enum.value_descriptions,
            )

            content = template.render(
                enum=enum_copy,
                class_name=class_name,
                version=self.schema.version.lstrip("v").lstrip("v"),
            )

            filename = f"{name}.py"
            (output_dir / filename).write_text(content)
            generated.append(class_name)

        return generated

    def _generate_objects(self, output_dir: Path) -> list[tuple[str, str]]:
        """Generate object model files.

        Returns:
            List of (class_name, original_name) tuples
        """
        template = self.env.get_template("object.py.jinja2")
        generated = []

        for name, obj in self.schema.objects.items():
            class_name = snake_to_pascal(name)

            # Process attributes
            attributes, imports = self._process_attributes(
                obj.attributes, "objects", current_class_name=class_name
            )

            content = template.render(
                object=obj,
                class_name=class_name,
                attributes=attributes,
                imports=sorted(set(imports)),
                has_optional_fields=any(not a.is_required for a in attributes),
                version=self.schema.version.lstrip("v"),
            )

            filename = f"{name}.py"
            (output_dir / filename).write_text(content)
            generated.append((class_name, name))

        return generated

    def _generate_events(self, output_dir: Path) -> list[tuple[str, str]]:
        """Generate event class files.

        Returns:
            List of (class_name, original_name) tuples
        """
        template = self.env.get_template("event.py.jinja2")
        generated = []

        for name, event in self.schema.events.items():
            # Skip base/abstract events
            if event.uid == 0:
                continue

            class_name = snake_to_pascal(name)

            # Process attributes (skip class_uid and category_uid - handled in template)
            filtered_attrs = {
                k: v for k, v in event.attributes.items() if k not in ("class_uid", "category_uid")
            }
            attributes, imports = self._process_attributes(
                filtered_attrs, "events", current_class_name=class_name
            )

            content = template.render(
                event=event,
                class_name=class_name,
                attributes=attributes,
                imports=sorted(set(imports)),
                version=self.schema.version.lstrip("v"),
            )

            filename = f"{name}.py"
            (output_dir / filename).write_text(content)
            generated.append((class_name, name))

        return generated

    def _process_attributes(
        self,
        attributes: dict[str, SchemaAttribute],
        context: str,
        current_class_name: str | None = None,
    ) -> tuple[list[FieldInfo], list[str]]:
        """Process attributes into FieldInfo objects and collect imports.

        Args:
            attributes: Dictionary of attributes to process
            context: Context string (e.g., "objects" or "events")
            current_class_name: Name of the class being generated (to skip self-references)
        """
        fields = []
        imports = []

        for name, attr in attributes.items():
            field_name = make_valid_identifier(name)

            # Determine type annotation
            enum_name = None
            if attr.enum:
                enum_name = name

            python_type = ocsf_type_to_python(
                attr.type,
                is_array=attr.is_array,
                object_type=attr.object_type,
                enum_name=enum_name,
            )

            # Make optional if not required
            is_required = attr.requirement == Requirement.REQUIRED
            type_annotation = f"{python_type} | None" if not is_required else python_type

            # Collect imports for referenced types
            if attr.object_type and attr.object_type in self.schema.objects:
                ref_class = snake_to_pascal(attr.object_type)
                # Skip self-references (class referencing itself)
                if ref_class != current_class_name:
                    imports.append(
                        f"from ocsf.{self.version_module}.objects.{attr.object_type} import {ref_class}"
                    )

            if enum_name and enum_name in self.schema.enums:
                enum_class = snake_to_pascal(enum_name)
                imports.append(
                    f"from ocsf.{self.version_module}.enums.{enum_name} import {enum_class}"
                )

            # Escape backslashes and quotes in description
            escaped_desc = (
                attr.description.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
            )

            fields.append(
                FieldInfo(
                    field_name=field_name,
                    type_annotation=type_annotation,
                    description=escaped_desc,
                    is_required=is_required,
                    requirement=attr.requirement.value,
                )
            )

        # Sort: required fields first, then by name
        fields.sort(key=lambda f: (not f.is_required, f.field_name))

        return fields, imports

    def _generate_init_files(
        self,
        version_dir: Path,
        enum_names: list[str],
        object_names: list[tuple[str, str]],
        event_names: list[tuple[str, str]],
    ) -> None:
        """Generate __init__.py files for all packages."""
        template = self.env.get_template("init.py.jinja2")

        # Enums __init__.py
        enum_imports = [
            f"from ocsf.{self.version_module}.enums.{self._class_to_module(name)} import {name}"
            for name in sorted(enum_names)
        ]
        content = template.render(
            description=f"OCSF {self.schema.version} enumerations.",
            imports=enum_imports,
            exports=sorted(enum_names),
        )
        (version_dir / "enums" / "__init__.py").write_text(content)

        # Objects __init__.py - use original names for imports
        object_imports = [
            f"from ocsf.{self.version_module}.objects.{orig_name} import {class_name}"
            for class_name, orig_name in sorted(object_names)
        ]
        object_exports = [class_name for class_name, _ in object_names]
        content = template.render(
            description=f"OCSF {self.schema.version} objects.",
            imports=object_imports,
            exports=sorted(object_exports),
        )
        (version_dir / "objects" / "__init__.py").write_text(content)

        # Events __init__.py - use original names for imports
        event_imports = [
            f"from ocsf.{self.version_module}.events.{orig_name} import {class_name}"
            for class_name, orig_name in sorted(event_names)
        ]
        event_exports = [class_name for class_name, _ in event_names]
        content = template.render(
            description=f"OCSF {self.schema.version} event classes.",
            imports=event_imports,
            exports=sorted(event_exports),
        )
        (version_dir / "events" / "__init__.py").write_text(content)

        # Version __init__.py
        all_exports = sorted(enum_names + object_exports + event_exports)
        # Generate explicit imports instead of star imports
        version_imports = []
        # Import enums explicitly
        for enum_name in sorted(enum_names):
            version_imports.append(f"from ocsf.{self.version_module}.enums import {enum_name}")
        # Import objects explicitly
        for class_name in sorted(object_exports):
            version_imports.append(f"from ocsf.{self.version_module}.objects import {class_name}")
        # Import events explicitly
        for class_name in sorted(event_exports):
            version_imports.append(f"from ocsf.{self.version_module}.events import {class_name}")
        # Build list of models to rebuild (objects and events, not enums)
        rebuild_models = [
            {"name": class_name, "is_model": True} for class_name in object_exports + event_exports
        ]
        content = template.render(
            description=f"OCSF {self.schema.version} Pydantic models.",
            imports=version_imports,
            exports=all_exports,
            rebuild_models=rebuild_models,
        )
        (version_dir / "__init__.py").write_text(content)

    def _class_to_module(self, class_name: str) -> str:
        """Convert PascalCase class name back to snake_case module name."""
        import re

        # Insert underscore before uppercase letters and lowercase everything
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", class_name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def generate_models(schema: ParsedSchema, output_dir: Path) -> None:
    """Generate all Pydantic models for a schema."""
    generator = ModelGenerator(schema, output_dir)
    generator.generate_all()


if __name__ == "__main__":
    import sys

    from generator.schema_parser import parse_schema

    version = sys.argv[1] if len(sys.argv) > 1 else "v1.2.0"
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("src/ocsf")
    cache = Path(".schema_cache")

    print(f"Parsing schema {version}...")
    schema = parse_schema(version, cache_dir=cache)

    print(f"Generating models to {output}...")
    generate_models(schema, output)

    print("Done!")
