### Metadata 

meta <- read.table("pubMLST_metadata.txt", header= T ,sep = '\t', fill = T )
hexMLST2 <- read.csv("hex_analysis/hexMLST2.csv", header = T, row.names="genomes")

meta_1 <- meta[,c(2,4,5,8)]
meta_1 <- meta_1[!duplicated(meta_1), ]


can_meta <- read.table("straindata_287.txt", sep = '\t', header = T)
can_meta <- can_meta[,c(1,3,10,2)]
colnames(can_meta) <- colnames(meta_1)
all_meta <- rbind(can_meta, meta_1)

matching_rows <- which(all_meta$isolate %in% row.names(hexMLST2))
meta_data <- all_meta[matching_rows, ]
get_rid <- (which(!(row.names(hexMLST2) %in% meta_data$isolate)))
fixed_hex <- hexMLST2[-get_rid,]
fixed_hex$st <- NA
fixed_hex$st <- 1:length(fixed_hex$st)

meta_data <- meta_data[!duplicated(meta_data[,1]),]
row.names(meta_data) <- meta_data$isolate
meta_data1 <- meta_data[,-1]
# length(which(meta_data$isolate %in% row.names(fixed_hex)))



write.table(fixed_hex, "fixed.hex.txt", sep = '\t')
write.table(meta_data, "fixed_metadata.txt", sep = '\t')







