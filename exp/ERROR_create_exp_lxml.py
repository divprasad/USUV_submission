#!/usr/bin/env python3
import sys
import argparse
from lxml import etree

# Helper function to create an EXPERIMENT_ATTRIBUTE
def create_experiment_attribute(parent, tag, value):
    """
    Create an EXPERIMENT_ATTRIBUTE XML element.
    """
    experiment_attr = etree.SubElement(parent, "EXPERIMENT_ATTRIBUTE")
    etree.SubElement(experiment_attr, "TAG").text = tag
    etree.SubElement(experiment_attr, "VALUE").text = value

def tsv2XML(tsvInFile, xmlOutFile):
    """
    Converts a TSV file into an XML file with the desired structure.
    """
    root = etree.Element("EXPERIMENT_SET")
    count = 0  # Line counter
    skip = 0  # Lines skipped

    try:
        with open(tsvInFile, 'r') as f:
            for line in f:
                line = line.rstrip()

                try:
                    #Unpack values from TSV
                    samAlias, expAlias, dumA, dumB, platform = line.split('\t')

                    # Check if any of the unpacked values is an empty string
                    if any(value == "" for value in [samAlias, expAlias, dumA, dumB, platform]):
                        print(f"Warning: Line {count+1} contains empty values. Skipping.")
                        count += 1
                        skip +=1
                        continue

                except ValueError:
                    print(f"Warning: Line {count+1} does not have the expected 5 tab-separated values. Skipping.")
                    count += 1
                    skip +=1
                    continue

                # Create EXPERIMENT element
                experiment = etree.SubElement(root, "EXPERIMENT", {
                    "alias": expAlias,
                    "center_name": "One Health Pact Consortium (2020–2022), EcoAlert Collaborative Team (2016–2019)"
                })

                # Add TITLE
                exp_title= str(platform) + " sequencing"
                etree.SubElement(experiment, "TITLE").text = str(exp_title)

                # Add STUDY_REF
                study_ref = etree.SubElement(experiment, "STUDY_REF")
                study_ref.attrib["accession"] = "PRJEB83966"

                # Add DESIGN
                design = etree.SubElement(experiment, "DESIGN")
                etree.SubElement(design, "DESIGN_DESCRIPTION").text = ""
                sample_descriptor = etree.SubElement(design, "SAMPLE_DESCRIPTOR")
                sample_descriptor.attrib["refname"] = samAlias

                library_descriptor = etree.SubElement(design, "LIBRARY_DESCRIPTOR")
                etree.SubElement(library_descriptor, "LIBRARY_NAME").text = ""
                etree.SubElement(library_descriptor, "LIBRARY_STRATEGY").text = "AMPLICON"
                etree.SubElement(library_descriptor, "LIBRARY_SOURCE").text = "VIRAL RNA"
                etree.SubElement(library_descriptor, "LIBRARY_SELECTION").text = "PCR"
                library_layout = etree.SubElement(library_descriptor, "LIBRARY_LAYOUT")
                etree.SubElement(library_layout, "SINGLE")

                # Add PLATFORM
                platform = etree.SubElement(experiment, "PLATFORM")
                oxford_nanopore = etree.SubElement(platform, "OXFORD_NANOPORE")
                etree.SubElement(oxford_nanopore, "INSTRUMENT_MODEL").text = platform

                # Add EXPERIMENT_ATTRIBUTES
                experiment_attributes = etree.SubElement(experiment, "EXPERIMENT_ATTRIBUTES")
                create_experiment_attribute(experiment_attributes, "library preparation date", "not collected")

                count += 1  # Increment processed line counter

    except FileNotFoundError:
        print(f"Error: The file '{tsvInFile}' does not exist.")
        sys.exit(1)

    # Format and write the XML to file using lxml
    tree = etree.ElementTree(root)
    with open(xmlOutFile, 'wb') as file:
        tree.write(file, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    return count - skip

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Convert a TSV file to an XML file with the desired experiment structure."
    )
    parser.add_argument("-i", "--input", help="Path to the input TSV file", required=True)
    parser.add_argument("-o", "--output", help="Path to the output XML file (optional)", default=None)

    # Parse arguments
    args = parser.parse_args()

    # Determine the output file name
    inFile = args.input
    if args.output:
        outFile = args.output
    else:
        outFile = inFile.rsplit('.', 1)[0] + '.xml'  # Change extension to _exp.xml

    # Execute the TSV to XML conversion
    try:
        COUNT = tsv2XML(inFile, outFile)
        print(f"\n{COUNT} EXPERIMENTS successfully written to {outFile} XML file")
    except FileNotFoundError:
        print(f"Error: The file '{inFile}' does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
