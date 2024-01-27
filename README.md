This package is a configuration loading tool for pyspark. Spark configs are specified in yaml with some examples in the conf folder. The primary entry point to loading spark is through the NewSparkSession class. Used like this:

```
from spark_loader.spark import NewSparkSession
 
sess = NewSparkSession('local', 'main', './conf/local.yaml')
```

The spark-nlp library is included, some workflow examples are with an initiated session are:

## Graph extraction

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

## LDA topic modeling

```
from sparknlp.base import  DocumentAssembler, Pipeline, Finisher
from sparknlp.annotator import (
  Normalizer, Tokenizer, StopWordsCleaner, Stemmer
)
from pyspark.ml.clustering import LDA
from pyspark.ml.feature import CountVectorizer
 
document_assembler = DocumentAssembler() \
    .setInputCol("value") \
    .setOutputCol("document") \
    .setCleanupMode("shrink")

tokenizer = Tokenizer() \
  .setInputCols(["document"]) \
  .setOutputCol("token")

normalizer = Normalizer() \
    .setInputCols(["token"]) \
    .setOutputCol("normalized")

stopwords_cleaner = StopWordsCleaner()\
      .setInputCols("normalized")\
      .setOutputCol("cleanTokens")\
      .setCaseSensitive(False)

stemmer = Stemmer() \
    .setInputCols(["cleanTokens"]) \
    .setOutputCol("stem")

finisher = Finisher() \
    .setInputCols(["stem"]) \
    .setOutputCols(["tokens"]) \
    .setOutputAsArray(True) \
    .setCleanAnnotations(False)

pipe = Pipeline(
    stages=[document_assembler, 
            tokenizer,
            normalizer,
            stopwords_cleaner, 
            stemmer, 
            finisher])

nlp_model = nlp_pipeline.fit(df)
processed_df  = nlp_model.transform(df)

cv = CountVectorizer(inputCol="tokens", outputCol="features", vocabSize=12000, minDF=3.0) 
cv_model = cv.fit(processed_df) 
vectorized_tokens = cv_model.transform(processed_df)

print("forming topics")

num_topics = 10
lda = LDA(k=num_topics, maxIter=50)
model = lda.fit(vectorized_tokens)
ll = model.logLikelihood(vectorized_tokens)
lp = model.logPerplexity(vectorized_tokens)
print("The lower bound on the log likelihood of the entire corpus: " + str(ll))
print("The upper bound on perplexity: " + str(lp))

```