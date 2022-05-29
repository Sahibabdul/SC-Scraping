#install prerequisites libraries
install.packages('ggfortify')
library(DescTools) 
library(tidyverse) 
library(readxl) 
library(fixest) 
library(dplyr) 
library(plyr) 
library(magrittr) 
library(psych) 
library(car) 
library(ggplot2)
library(ggfortify)
library(ggfo)
library(dplyr)
library(stats)


#reading data-file:
SoComp_clean_datasheet <- read_csv("SoComp_clean_datasheet.csv")


#Processing of the Data_
##Dummy-Coding for Verdict:
SoComp_clean_datasheet$verdict_dummy <- ifelse(SoComp_clean_datasheet$verdict == "YES", 1, 0)
## Removing special character signs from values:
SoComp_clean_datasheet$voter_turnout <- gsub("%$","",SoComp_clean_datasheet$voter_turnout)
SoComp_clean_datasheet$voter_turnout <- as.numeric(SoComp_clean_datasheet$voter_turnout)


SoComp_clean_datasheet$voting_result <- gsub("%$","",SoComp_clean_datasheet$voting_result)
SoComp_clean_datasheet$voting_result <- as.numeric(SoComp_clean_datasheet$voting_result)


SoComp_clean_datasheet$yes_ads <- gsub("%$","",SoComp_clean_datasheet$yes_ads)
SoComp_clean_datasheet$yes_ads <- as.numeric(SoComp_clean_datasheet$yes_ads)


SoComp_clean_datasheet$'20m_nof_commentators'<- gsub("[^[:alnum:]]", "",SoComp_clean_datasheet$'20m_nof_commentators')
SoComp_clean_datasheet$'20m_nof_commentators' <- as.numeric(SoComp_clean_datasheet$'20m_nof_commentators')


#Create 20Min-Dataframe for analysis:
zwanzig_df <- SoComp_clean_datasheet[,c(1,4,6:15, 23:40)]
subset_zwanzig <- subset(zwanzig_df, select = c(1,2,4:6,9:12,14:30))


#cronbachs alpha via psych package to measure if latent constructs are valid 
cronbach_alpha_zwanzig <- alpha(subset_zwanzig, na.rm=TRUE) 
cronbach_alpha_zwanzig


#20Min-Descriptive statistics:
describeBy(subset_zwanzig)
summary(subset_zwanzig)
str(subset_zwanzig)


#shapiro test Normalverteilung
shapiro.test(rstandard(modell_1a))

#20Min: Correlationmatrix
##Spearman correlationkoefficient --> not all the variables metrical, bi-variate normal distribution not fullfilled
cor_zwanzig <- cor(subset_zwanzig, method = "spearman")
write.table(cor_zwanzig, file = "correlationmatrix_spearman_20min.csv", sep = ",", quote = FALSE, row.names = F)

corrplot(cor_zwanzig, method = "color", type="lower", title="Correlationmatrix")




install.packages("correlation")
library(correlation)
cor_zwanzig_II <- correlation(subset_zwanzig, method = "spearman")
cor_zwanzig_II

summary(correlation(subset_zwanzig))
# for apa format of the table --> apa.cor.table(cor_zwanzig, filename='test')










