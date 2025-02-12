from lxml import etree
import sys
import argparse


"""
Usage: create_sam_lxml.py [-h] -i INPUT

Convert a `sam.tsv` file into a `sam.xml` file with the required structure for submitting a sample metadata object to ENA.

Options:
  -h, --help            Help message.
  -i INPUT, --input INPUT
                        Specify the path to the input TSV file containing sample metadata.
                        The file must include all required fields for generating the sample metadata XML.

# CHECK LIST


"""






# Helper function to create a SAMPLE_ATTRIBUTE
def create_sample_attribute(parent, tag, value, units=None):
    """
    Create a SAMPLE_ATTRIBUTE XML element.
    """
    sample_attr = etree.SubElement(parent, "SAMPLE_ATTRIBUTE")
    etree.SubElement(sample_attr, "TAG").text = tag
    etree.SubElement(sample_attr, "VALUE").text = value
    if units:
        etree.SubElement(sample_attr, "UNITS").text = units

def tsv2XML(tsvInFile, xmlOutFile):
    """
    Convert a TSV file into an XML file with the required structure.
    """
    root = etree.Element("SAMPLE_SET")
    line_counter = 0  # Total lines processed
    skipped_lines= 0   # Number of skipped lines (header, errors, or incomplete data)

    try:
        with open(tsvInFile, 'r') as f:
            for line in f:
                line_counter += 1
                line = line.strip()

                # skip empty or malformed lines (not exactly 16 tab-separated values)
                if not line or len(line.split('\t')) != 16:
                    print(f"Warning: Skipping malformed or incomplete line {line_counter}.")
                    skipped_lines+= 1
                    continue

                # skip lines containing "alias" (header or irrelevant)
                if "alias" in line:
                    skipped_lines+= 1
                    print("Skipping header")
                    continue

                try:
                    # Extract required values from TSV (expecting exactly 16 tab-separated fields)
                    (
                        insdc_acc, sam_title, isolate, date,
                        alias, region, host_sex, host_sc,
                        host_comm, iso_host, lat, long,
                        host_disease_out, host_health_stat, host_sub_id, pub
                    ) = line.split('\t')

                    # Ensure required fields are not empty
                    required_fields = [
                        insdc_acc, sam_title, isolate, date, alias, region, host_sex, host_sc,
                        host_comm, iso_host, lat, long, host_disease_out, host_health_stat, host_sub_id, pub
                    ]
                    if not all(required_fields):
                        print(f"Warning: Line {line_counter} contains empty values. Skipping.")
                        skipped_lines += 1
                        continue

                except ValueError:
                    print(f"Warning: Line {line_counter} does not have the expected 16 tab-separated values. Skipping.")
                    skipped_lines +=1
                    continue

                # Create SAMPLE element
                sample = etree.SubElement(root, "SAMPLE", {"alias": alias, "center_name": "One Health Pact Consortium (2020–2022), EcoAlert Collaborative Team (2016–2019)"})

                # Add TITLE
                etree.SubElement(sample, "TITLE").text = sam_title

                # Add SAMPLE_NAME
                sample_name = etree.SubElement(sample, "SAMPLE_NAME")
                etree.SubElement(sample_name, "TAXON_ID").text = "64286"
                etree.SubElement(sample_name, "SCIENTIFIC_NAME").text = "Usutu virus"
                etree.SubElement(sample_name, "COMMON_NAME").text = "Usutu virus"

                # Mapping keywords to specific descriptions
                description_mapping = {
                    "blood": "Human blood donor samples testing RT-PCR positive for Usutu virus (CT values below 32) "
                             "were subjected to whole-genome sequencing using an amplicon-based Oxford Nanopore approach.",
                    "mosquitoes": "Mosquito samples testing RT-PCR positive for Usutu virus (CT values below 32) "
                                  "were subjected to whole-genome sequencing using an amplicon-based Oxford Nanopore approach.",
                    "free-ranging": "Samples from free-ranging birds testing RT-PCR positive for Usutu virus (CT values below 32) "
                                    "were subjected to whole-genome sequencing using an amplicon-based Oxford Nanopore approach.",
                    "captivity": "Samples from birds in captivity testing RT-PCR positive for Usutu virus (CT values below 32) "
                                 "were subjected to whole-genome sequencing using an amplicon-based Oxford Nanopore approach."
                }

                # Default description
                default_description = (
                    "Samples collected from humans (blood donors), wildlife (birds and mosquitoes), and captive birds in the Netherlands "
                    "that tested RT-PCR positive for Usutu virus (CT values below 32) were subjected to whole-genome sequencing using an "
                    "amplicon-based Oxford Nanopore approach."
                )

                # Determine the description based on sam_title
                description = next(
                    (desc for keyword, desc in description_mapping.items() if keyword in sam_title),
                    default_description
                )

                # Add DESCRIPTION
                etree.SubElement(sample, "DESCRIPTION").text = description

                # Add SAMPLE_ATTRIBUTES
                sample_attributes = etree.SubElement(sample, "SAMPLE_ATTRIBUTES")
                create_sample_attribute(sample_attributes, "collecting institution", "One Health Pact Consortium (2020–2022), EcoAlert Collaborative Team (2016–2019)") #One Health PACT Usutu virus workgroup
                create_sample_attribute(sample_attributes, "collection date", date)
                create_sample_attribute(sample_attributes, "collector name", "One Health Pact Consortium (2020–2022), EcoAlert Collaborative Team (2016–2019)")
                create_sample_attribute(sample_attributes, "geographic location (country and/or sea)", "Netherlands")
                if region != "IGNORE": # Add optional attributes if applicable
                    create_sample_attribute(sample_attributes, "geographic location (region and locality)", region)
                create_sample_attribute(sample_attributes, "geographic location (latitude)", lat, "DD")
                create_sample_attribute(sample_attributes, "geographic location (longitude)", long, "DD")
                create_sample_attribute(sample_attributes, "sample capture status", "active surveillance not initiated by an outbreak")
                if iso_host != "IGNORE": # Add optional attributes if applicable
                    create_sample_attribute(sample_attributes, "isolation source host-associated", iso_host)
                create_sample_attribute(sample_attributes, "host scientific name", host_sc)
                create_sample_attribute(sample_attributes, "host common name", host_comm)
                create_sample_attribute(sample_attributes, "host health state", host_health_stat)
                if host_disease_out != "IGNORE": # Add optional attributes if applicable
                    create_sample_attribute(sample_attributes, "host disease outcome", host_disease_out)
                create_sample_attribute(sample_attributes, "host sex", host_sex)
                create_sample_attribute(sample_attributes, "host subject id", host_sub_id)
                create_sample_attribute(sample_attributes, "isolate", isolate)
                create_sample_attribute(sample_attributes, "publication", pub)
                if insdc_acc != "IGNORE": # Add optional attributes if applicable
                    create_sample_attribute(sample_attributes, "INSDC accession", insdc_acc)
                create_sample_attribute(sample_attributes, "ENA-CHECKLIST", "ERC000033")

    except FileNotFoundError:
        print(f"Error: The file '{tsvInFile}' does not exist.")
        sys.exit(1)

    # Format and write the XML to file using lxml
    tree = etree.ElementTree(root)
    with open(xmlOutFile, 'wb') as file:
        tree.write(file, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    written = line_counter - skipped_lines
    return written

# Main execution
if __name__ == '__main__':

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Convert a `sam.tsv` file into a `sam.xml` file with the required structure for submitting a sample metadata object to ENA."
    )
    parser.add_argument(
        "-i", "--input",
        help="Specify the path to the input TSV file containing sample metadata. "
             "The file must include all required fields for generating the sam metadata XML.",
        default="sam.tsv"
    )

    # Parse arguments
    args = parser.parse_args()
    inFile = args.input  # Input file name
    outFile ="sam.xml"   # Input file name

    # Execute the TSV to XML conversion
    try:
        COUNT=tsv2XML(inFile, outFile)
        print(f"    {COUNT} sample_objects successfully written to '{outFile}'.")
    except FileNotFoundError:
        print(f"    Error: The file '{inFile}' does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"    An unexpected error occurred: {e}")
        sys.exit(1)
