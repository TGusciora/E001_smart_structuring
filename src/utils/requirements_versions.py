import os
import pkg_resources

def requirements_versions(output_file='requirements_versions.txt'):
    """
    Generates a custom requirements.txt file with versions for packages listed in a given requirements file.
    Directly includes comments and editable installs.
    
    Args:
    - output_file (str): Path to the output custom_requirements.txt file. Default is 'custom_requirements.txt'.
    
    Returns:
    None
    
    Raises:
    None
    """
    source_requirements =  os.path.join(os.path.dirname(os.getcwd()), 'requirements.txt')
    output_file = os.path.join(os.getcwd(), output_file)
    requirements = []

    with open(source_requirements, 'r') as file:
        for line in file:
            clean_line = line.strip()
            # Directly rewrite comments and editable installs
            if clean_line.startswith('#') or clean_line.startswith('-e'):
                requirements.append(clean_line)
                continue
            
            # Handle packages followed by comments
            package_name = clean_line.split('#')[0].strip()
            if package_name:
                try:
                    version = pkg_resources.get_distribution(package_name).version
                    requirements.append(f"{package_name}=={version}")
                except pkg_resources.DistributionNotFound:
                    print(f"Package {package_name} not found. Skipping...")
            else:
                # This handles the case where there's a comment after an empty package name
                if clean_line.endswith('#'):
                    requirements.append(clean_line)

    # Write the requirements to the output file, including comments and editable installs
    with open(output_file, 'w') as f:
        for requirement in requirements:
            f.write(f"{requirement}\n")

    print(f"Custom requirements.txt generated successfully at {output_file}")
