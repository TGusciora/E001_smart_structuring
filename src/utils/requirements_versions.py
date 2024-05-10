import os

import pkg_resources


def requirements_versions(output_file="requirements_versions.txt"):
    """
    Generates a custom requirements.txt file with versions for packages listed in a given requirements file.
    Directly includes comments, editable installs, and blank lines. Replaces any existing version specifier with the installed version.

    Args:
    - output_file (str): Path to the output requirements_versions.txt file.

    Returns:
    None

    Raises:
    None
    """
    source_requirements = os.path.join(
        os.path.dirname(os.getcwd()), "requirements.txt"
    )
    output_file = os.path.join(os.getcwd(), output_file)
    requirements = []

    with open(source_requirements, "r") as file:
        for line in file:
            clean_line = line.strip()
            # Handle blank lines by appending them directly
            if not clean_line:
                requirements.append("")
                continue
            # Directly rewrite comments and editable installs
            if clean_line.startswith("#") or clean_line.startswith("-e"):
                requirements.append(clean_line)
                continue

            # Split line at the first occurrence of '==' or ' ' or comments to handle version specifiers or options
            package_part = (
                clean_line.split("==")[0].split(" ")[0].split("#")[0].strip()
            )
            if package_part:
                try:
                    # Retrieve the installed version of the package
                    version = pkg_resources.get_distribution(
                        package_part
                    ).version
                    # Append the package and its installed version
                    requirements.append(f"{package_part}=={version}")
                except pkg_resources.DistributionNotFound:
                    print(f"Package {package_part} not found. Skipping...")
            else:
                # This handles the case where there's a comment after an empty
                # package name
                if clean_line.endswith("#"):
                    requirements.append(clean_line)

    # Write the requirements to the output file, including comments, editable
    # installs, and blank lines
    with open(output_file, "w") as f:
        for requirement in requirements:
            # Preserve blank lines in the output file
            if requirement == "":
                f.write("\n")
            else:
                f.write(f"{requirement}\n")

    print(f"Custom requirements.txt generated successfully at {output_file}")
