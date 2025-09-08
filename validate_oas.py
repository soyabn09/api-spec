import sys
import yaml
from openapi_spec_validator import validate_spec, openapi_v30_spec_validator
from openapi_spec_validator import openapi_v30_spec_validator as validator


def main(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    try:
        validate_spec(spec, validator=openapi_v30_spec_validator)
        print("Validation OK")
        return 0
    except Exception as e:
        print("Validation failed:\n", repr(e))
        try:
            errs = list(validator.iter_errors(spec))
            print(f"Error count: {len(errs)}")
            for i, err in enumerate(errs[:50]):
                print(f"[{i}] {err}")
                sp = getattr(err, "schema_path", None)
                ip = getattr(err, "path", None)
                print(" schema_path:", sp)
                print(" instance_path:", ip)
        except Exception as e2:
            print("Unable to iterate errors:", repr(e2))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "cherrytree.yaml"))
