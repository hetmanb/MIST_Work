#### MIST Workspace ####
library(reshape2)
library(reshape)


# Commands used to generate and Parse the MLST Data: 
# Run MIST 
system("cd /Users/bh/Dropbox/0\ -\ publications_bh/Shiny/MIST_Work/all_fasta/ && parallel mono ~/Temp/Release/MIST.exe -T /tmp/mist_tmp -t ~/Temp/Release/campylobacter_jejuni/MLST.markers -a ~/Temp/Release/campylobacter_jejuni/updated_mlst -c 4 -j MLST_{}.json {} ::: *.fasta")

MLST_results <- read.table("MLST_Results.csv", sep = '\t', header = T)
MLST <- MLST_results
# Convert long form data into readable table form and write to txt
MLST <- dcast(MLST, Strain~Marker, value.var = "Call")
write.table(MLST, paste("MLST_", length(MLST[,1]), ".txt", sep = ''), sep = '\t', row.names = MLST[,1])


#Commands used for hexMLST MIST Assay: 
system("parallel mono ~/Temp/mist/bin/Release/MIST.exe -T /Volumes/MERLIN/tmp -t ../campylobacter_jejuni/hexMLST.markers -a ../updated_hex_alleles/ -c 4 -j hexMLST_{}.json {} ::: *.fasta")
hexMLST_results <- read.table("MLST_Results.csv", sep = '\t', header = T)
hexMLST <- MLST_results
#Parse from long format to readable table: 
hexMLST <- dcast(MLST, Strain~Marker, value.var = "Call")
write.table(hexMLST, paste("hexMLST_", length(hexMLST[,1]), ".txt", sep = ''), sep = '\t', row.names = hexMLST[,1])


#Checks the difference between the original hex files and the 2nd iteration (after updating the alleles)
orig_hex <- list.files("hexMLST_JSON/")
new_hex <- list.files("hexMLST_JSON_2/")

orig_hex[!(orig_hex %in% new_hex)]

#Read the .csv of the resulting hexMLST calls back into R: 
hexMLST2 <- read.csv("hexMLST2.csv", header = T, row.names="genomes")



