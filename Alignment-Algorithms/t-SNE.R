# loads all packages
library("Rtsne")
library(readxl)
library(ggplot2)
library(rgl)
library(rglwidget)
library(htmltools)
library(pandoc)

# generates the t-SNE visualisation objects and saves them in a data frame
data <-(Fingerprint2)
print(data)
row.names <-data$BaseText
data_matrix <- as.matrix(data[,-1])
num_rows <- nrow(data_matrix)
perplexity_value <- min(30, num_rows / 2)
perplexity_value <- 3
print(paste("Chosen perplexity value:", perplexity_value))
tsne_results <- Rtsne(data_matrix, dims=3, perplexity = perplexity_value, theta=0.5, check_duplicates = FALSE)
tsne_data <- as.data.frame(tsne_results$Y)

# plots the t-SNE on a 3D graph with labels
plot3d(x=tsne_results$Y[,1], y=tsne_results$Y[,2], z=tsne_results$Y[,3], type='p', size=7)
text3d(x=tsne_results$Y[,1], y=tsne_results$Y[,2], z=tsne_results$Y[,3], texts=data$BaseText, adj=2)

# generates an interactive widget of the graph within an HTML file that can be saved and shared.
save <-getOption("rgl.useNULL")
options(rgl.useNULL=TRUE)
widget <-rglwidget(x=scene3d(), width=figWidth(), height=figHeight(), controllers=NULL, snapshot=FALSE, 
                   elementId = NULL, reuse = !interactive(), webGLoptions = list(preserveDrawingBuffer = TRUE))
filename <-tempfile(fileext = ".html")
htmlwidgets::saveWidget(widget, filename)
browseURL(filename)

# generates a 2D plot of the t-SNE data (can be misleading)
colnames(tsne_data) <- c("TSNE1", "TSNE2")
tsne_data$Manuscript <- data$BaseText
ggplot(tsne_data, aes(x = TSNE1, y = TSNE2, label = Manuscript)) +
  geom_text(size = 3, vjust = 1, hjust = 1) + geom_point() +
  ggtitle("t-SNE: Italian Family") +
  xlab("t-SNE Dimension 1") +
  ylab("t-SNE Dimension 2")
