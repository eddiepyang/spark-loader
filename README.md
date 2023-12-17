Load session prior to running
```
from sparknlp.base import  DocumentAssembler, Pipeline
from sparknlp.annotator import (
    NerDLModel, NerDLApproach, 
    GraphExtraction, UniversalSentenceEncoder,
    Tokenizer, WordEmbeddingsModel
)


# load spark session before this

use = UniversalSentenceEncoder \
    .pretrained() \
    .setInputCols("document") \
    .setOutputCol("use_embeddings")

document_assembler = DocumentAssembler() \
    .setInputCol("value") \
    .setOutputCol("document")

tokenizer = Tokenizer() \
    .setInputCols(["document"]) \
    .setOutputCol("token")

word_embeddings = WordEmbeddingsModel \
    .pretrained() \
    .setInputCols(["document", "token"]) \
    .setOutputCol("embeddings")


ner_tagger = NerDLModel \
    .pretrained() \
    .setInputCols(["document", "token", "embeddings"]) \
    .setOutputCol("ner")

graph_extraction = GraphExtraction() \
            .setInputCols(["document", "token", "ner"]) \
            .setOutputCol("graph") \
            .setRelationshipTypes(["lad-PER", "lad-LOC"]) \
            .setMergeEntities(True)

graph_pipeline = Pipeline() \
    .setStages([
        document_assembler, tokenizer,
        word_embeddings, ner_tagger,
        graph_extraction
    ])

df = sess.read.text('./data/train.dat')
graph_pipeline.fit(df).transform(df)
```
