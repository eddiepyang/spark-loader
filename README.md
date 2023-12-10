Load session prior to running
```import sparknlp
from sparknlp.base import *
from sparknlp.annotator import *
from pyspark.sql import SparkSession


# load spark session before this
use = UniversalSentenceEncoder \
    .pretrained("tfhub_use_multi", "xx") \
    .setInputCols("document") \
    .setOutputCol("use_embeddings")
document_assembler = DocumentAssembler().setInputCol("value").setOutputCol("document")

tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")

word_embeddings = WordEmbeddingsModel.pretrained() \
    .setInputCols(["document", "token"]) \
    .setOutputCol("embeddings")

ner_tagger = NerDLModel.pretrained() \
    .setInputCols(["document", "token", "embeddings"]) \
    .setOutputCol("ner")

graph_extraction = GraphExtraction() \
            .setInputCols(["document", "token", "ner"]) \
            .setOutputCol("graph") \
            .setRelationshipTypes(["lad-PER", "lad-LOC"]) \
            .setMergeEntities(True)

graph_pipeline = Pipeline().setStages([document_assembler, tokenizer,
                                       word_embeddings, ner_tagger,
                                       graph_extraction])

res_df = graph_pipeline.fit(df).transform(df)
```