## R Script for generating clusters and dist trees of hexMLST results

#Read the .csv of the resulting hexMLST calls back into R: 
hexMLST2 <- read.csv("hex_analysis/hexMLST2.csv", header = T, row.names="genomes")
# write.table(hexMLST2, "hexMLST2.txt", sep = '\t')
hex_dist <- dist(hexMLST2, )
# Compute the pairwise similarity scores for each of the genomes hex-scores: 
library(ape)
pairwise_sim <- dist.gene(hexMLST2, method = 'pairwise')

hc_hex <- hclust(pairwise_sim)

# plot(as.dendrogram(hc_hex))

full_cut <- cutree(hc_hex, h = 1*max(hc_hex$height))
ninetyfive_cut <- cutree(hc_hex, h = 0.95*max(hc_hex$height))
ninety_cut <- cutree(hc_hex, h = 0.9*max(hc_hex$height))
eightyfive_cut <- cutree(hc_hex, h = 0.85*max(hc_hex$height))


