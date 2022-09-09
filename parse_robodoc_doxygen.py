import glob
import in_place


def main():
    # FOLDER='/home/jain/projects/Flash-X/source/Driver/**/*.F90'
    # FOLDER='/home/jain/projects/Flash-X/source/flashUtilities/**/*.F90'
    # FOLDER='/home/jain/projects/Flash-X/source/Grid/**/*.F90'
    # change this as needed <> **
    FOLDER = '/home/jain/projects/Flash-X/source/Particles/ParticlesMapping/MeshOwned/Quadratic/pt_mapFromMeshQuadratic.F90'

    f_files = []
    for name in glob.iglob(FOLDER, recursive=True):
        f_files.append(name)

    print(f_files)

    # f_files=[]
    # f_files.append("source/Grid/GridMain/UG/Grid_iterator.F90")

    for f in f_files:
        # <> ** uncomment below print to see files selected.
        # print(f)
        name = False
        synopsis = False
        arguments = False
        details = False
        headerWritten = False
        notice = 0

        j = 0
        with in_place.InPlace(f) as fhandle:
            lines = fhandle.readlines()
            for line in lines:
                #  print(line)
                if (line.__contains__("!!****f") or
                        line.__contains__("!!****i") or
                        line.__contains__("!!***v") or
                        line.__contains__("!!***f") or
                        line.__contains__("!!****h") or
                        line.__contains__("!!****v") or
                        line.__contains__("!!****c") or
                        line.__contains__("!!****m")):
                    #  skip this line from writing
                    j += 1
                    print(line)
                    # skip 11 notice lines of robodoc format
                elif (line.__contains__("!! NOTICE")):
                    notice += 1
                    j += 1
                elif (notice > 0 and notice < 11):
                    notice += 1
                    j += 1
                elif (line.__contains__("NAME") and
                      line.lstrip().startswith("!")):
                    name = True
                    j += 1
                    print(line)
                elif (name == True and line.__contains__("SYNOPSIS") and
                      line.lstrip().startswith("!")):
                    synopsis = True
                    name = False
                    j += 1
                    print(line)
                elif ((line.__contains__("FUNCTION") or
                       line.__contains__("DESCRIPTION")) and
                      details == False and line.lstrip().startswith("!")):
                    synopsis = False
                    name = False
                    details = True
                    #
                    if headerWritten == False:
                        headerWritten = writeHeader(headerWritten, fhandle)

                    fhandle.write("!> \n!! @details\n")

                    j += 1
                    print(line)
                elif (line.__contains__("ARGUMENTS") and details == False and
                      line.lstrip().startswith("!")):
                    synopsis = False
                    name = False
                    details = True

                    #
                    if headerWritten == False:
                        headerWritten = writeHeader(headerWritten, fhandle)

                    fhandle.write("!> \n!! @details\n")
                    j += 1
                    print(line)
                elif (
                    (name == True or synopsis == True) and details == False and
                        line.lstrip().startswith("!")
                ):  #this is important as description sets name and synopsis to False
                    j += 1
                    # skip
                    print(line)
                elif (j >= 0 and (line.__contains__("!!***") or
                                  line.__contains__("!!****"))):
                    #   if it got here, set details to true so the rest can be written
                    details = True
                    synopsis = False
                    name = False
                    if line.__contains__("!!*****"):  #bigger comment line
                        j += 1
                        fhandle.write(line)
                    else:
                        j += 1
                        print(line)
                else:
                    fhandle.write(line)
                    name = False
                    synopsis = False
                    arguments = False
                    details = False


def writeHeader(headerWritten, fhandle):
    text = "!> @copyright Copyright 2022 UChicago Argonne, LLC and contributors \n!! \n!! @licenseblock\n!! Licensed under the Apache License, Version 2.0 (the \"License\");\n!! you may not use this file except in compliance with the License.!!\n!! Unless required by applicable law or agreed to in writing, software\n!! distributed under the License is distributed on an \"AS IS\" BASIS,\n!! WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n!! See the License for the specific language governing permissions and\n!! limitations under the License.\n!! @endlicenseblock\"\n"
    if headerWritten == False:
        fhandle.write(text)

    headerWritten = True
    return headerWritten


if __name__ == "__main__":
    main()

# c_files = []
# for name in glob.iglob('/home/jain/projects/Flash-X/source/**/*.c',recursive = True):
#     c_files.append(name)

# # print(c_files)

# h_files = []
# for name in glob.iglob('/home/jain/projects/Flash-X/source/**/*.h',recursive = True):
#     h_files.append(name)
