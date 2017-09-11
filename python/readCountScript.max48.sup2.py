#!/usr/bin/python2.7

"""
Supplementary Note 2: Center Weighting

Authors: Eugene Oh, Annemarie Becker

inputFile:
.map file generated by Bowtie default output.

outputFileP:
read density file for plus strand
    col0: position along genome
    col1: read density at that position

outputFileM:
read density file for minus strand
    col0: position along genome
    col1: read density at that position

"""


def rawdata(inputFile, outputFileP, outputFileM, min_length, max_length):

    pDict = {}
    mDict = {}

    inFile = open(inputFile, 'r')
    line = inFile.readline()
    while line != '':
        fields = line.split()
        col2 = str(fields[2])   #strand; note: if sequencing was performed without barcode reading, the column numbering is changed
        col4 = int(fields[4])   #left-most position
        col5 = str(fields[5])   #footprint seq
        length = len(col5)      #footprint length

        center_offset = int((min_length-1)/2) #center for min_length always 1 or 2 nt

        if min_length <= length <= max_length:    #select range of footprint read lengths
            if col2 == '+':	#for plus strand
                columns = len(fields)   #count number of columns to check if alignment contains mismatches
                if columns > 8:
                    col8 = str(fields[8])
                    if col8.startswith("0"):	#if there is a mismatch in the 1st position
                        length0 = length - 1    #subtract wrong base at 1st position
                        end5 = col4 + 2		#Bowtie uses 0-based offset: transform to 1-based and subtract 1st base
                        end3 = end5 + length0 - 1
                        centerEnd5 = end5 + center_offset	#define center
                        centerEnd3 = end3 - center_offset
                        centerLength = centerEnd3 - centerEnd5 + 1
                    else:
                        end5 = col4 + 1     #Bowtie uses zero-based offset, transform to 1-based
                        end3 = end5 + length - 1
                        centerEnd5 = end5 + center_offset
                        centerEnd3 = end3 - center_offset
                        centerLength = centerEnd3 - centerEnd5 + 1
                else:
                    end5 = col4 + 1
                    end3 = end5 + length - 1
                    centerEnd5 = end5 + center_offset
                    centerEnd3 = end3 - center_offset
                    centerLength = centerEnd3 - centerEnd5 + 1

                for elem in range(centerEnd5, centerEnd3 + 1):
                    if elem in pDict:
                        pDict[elem] += (1.0 / centerLength)
                    else:
                        pDict[elem] = (1.0 / centerLength)

            elif col2 == '-':		#for minus strand
                columns = len(fields)
                if columns > 8:
                    col8 = str(fields[8])
                    if col8.startswith("0"):
                        length0 = length - 1
                        end3 = col4 + 1         #for minus strand, Bowtie gives leftmost position (3' end) with zero-based numbering
                        end5 = end3 + length0 - 1
                        centerEnd5 = end5 - center_offset
                        centerEnd3 = end3 + center_offset
                        centerLength = centerEnd5 - centerEnd3 + 1
                    else:
                        end3 = col4 + 1
                        end5 = end3 + length - 1
                        centerEnd5 = end5 - center_offset
                        centerEnd3 = end3 + center_offset
                        centerLength = centerEnd5 - centerEnd3 + 1
                else:
                    end3 = col4 + 1
                    end5 = end3 + length - 1
                    centerEnd5 = end5 - center_offset
                    centerEnd3 = end3 + center_offset
                    centerLength = centerEnd5 - centerEnd3 + 1

                for elem in range(centerEnd3, centerEnd5 + 1):
                    if elem in mDict:
                        mDict[elem] += (1.0 / centerLength)
                    else:
                        mDict[elem] = (1.0 / centerLength)

        line = inFile.readline()

    pList = pDict.items()
    pList.sort()
    outFileP = open(outputFileP, 'w')
    for J in pList:
        outFileP.write(str(J[0]) + '\t' + str(J[1]) + '\n')

    mList = mDict.items()
    mList.sort()
    outFileM = open(outputFileM, 'w')
    for J in mList:
        outFileM.write(str(J[0]) + '\t' + str(J[1]) + '\n')


if __name__=='__main__':
    # Parse commandline arguments
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--infile', help='Input file (bwt).')
    parser.add_argument('--outP', help='Output file P.')
    parser.add_argument('--outM', help='Output file M.')
    parser.add_argument('--min', help='Min. length.', type=int)
    parser.add_argument('--max', help='Max. length.', type=int)

    args = parser.parse_args()

    inputFile = args.infile
    outputFileP = args.outP
    outputFileM = args.outM
    min_length = args.min
    max_length = args.max

    rawdata(inputFile, outputFileP, outputFileM, min_length, max_length)
