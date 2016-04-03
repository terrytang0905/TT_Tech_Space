---
layout: post
category : datascience
tags : [search, bigdata, develop]
title: FullText Search Design Note - Lucene 
---
{% include JB/setup %}

Beginning from Aug in 2009, I have involved into one fulltext search engine project in EMC content management division. The search engine is based on lucene tech as the core architecture and adopt xDB NoSQL DB (One XML database occupied by EMC) to store big unstructured data. After this project,I also took other related cross research about full text implementation (ElasticSearch) and the popular NoSQL DB MongoDB and adopt the related tech to design and implement open source search engine in one mobile internet project from Lenovo. At the end I try to reorganize my understanding for fulltext search and write down the principle of designing and architecture for common fulltext search engine. All contents follow lucene design philosophy and use lucene as the main example.

### FullText Search Architecture
Here are the following main function aspects for fulltext search engine. I will explain every function step by step later.

1. Index/Information Crawler: Data comes from database / webpage / document
Solution: Scrapy

2. Content Extractor/Text Extractor: extract fulltext from any media.
Solution: Oracle OutSide In 

3. Content Analysis/Tokenization: automatic language detection, stemming, lemmatization
Solution: Basis / Tika / Snowball / Lucene Analysis

4. Search Engine Management: It used to call and manage the index/query task accordingly and included that Index/Search/Query Modules.
Solution: xPlore IndexServer/ElasticSearch/Sphinx(for SQL)

5. Core Index&Search Design: lucene
Transform any fulltext data to lucene document format (XML to lucene document)
Solution: Lucene multiple index(Concurrent Index / Parallel Query)

6. Quality of Search 
- Scoring(Similarity & Relevance)/ Sorting & Ranking
- Summary result / Highlighting keyword
- Possible Query language for Advanced operators
- Possible Query language for structured searches
- MoreLikeThis / Fuzzy Search
- Spell check / Recommendation
- Scale out / Horizontal scaling (Multi-Node / SharedIndex / Sharding & Share Nothing)
- Ingest/Query Time Performance
- Space consumption performance

7. BigData storage & Analysis: store any index meta data or source contents
Solution: FileSystem / Hadoop or GFS or TFS / NoSQL DB (xDB & MongoDB) 

### lucene Design Principle & Architecture

Quick search repeatly based on one index

Tokenizer
Stop Word
Send Token to Linguistic Processor included Lowercase/stemming/lemmatization
Create Term and import into Indexer

Indexer: 
Document Frequency / Term Frequency in the specific document 
Query Analyer / QueryParser
Term Weight
TF-IDF module

#### Lucene Index

- Index processing:
1. 创建一个IndexWriter用来写索引文件,它有几个参数,INDEX_DIR就是索引文件所存放的位
置,Analyzer便是用来对文档进行词法分析和语言处理的。
2. 创建一个Document代表我们要索引的文档。
3. 将不同的Field加入到文档中。我们知道,一篇文档有多种信息,如题目,作者,修改时间,内
容等。不同类型的信息用不同的Field来表示,在本例子中,一共有两类信息进行了索引,一个
是文件路径,一个是文件内容。其中FileReader的SRC_FILE就表示要索引的源文件。
4. IndexWriter调用函数addDocument将索引写到索引文件夹中。

- Inverted Index:

    Term->Fields->Segments->Index
    Term->TermPostingList (DocumentID/TF/Position/Payload)
	Segment 
	Write.lock (Sync index info during merging)
	Field: .fdt .fdx
	TermVector .tvx .tvd
	Term Dictionary  .tis .tii .frq .prx 
	Term Weight & Score: .nrm (Normalization Factor:Document boost/Field boost/lengthNorm(field))
	Blacklist/Delete Document: .del
	Merge and compound file(.cfs) / ConcurrentMergeScheduler

- IndexWriter:

- IndexChain:

	DocFieldProcessor:
		DocConsumer consumer 
		deletesInRAM and deletesFlushed
		RAMBuffer management
		Multi-thread concurrent indexING (sync index docID)
		Add document into Index synchronizely
		DocumentsWriterThreadState
	DocFieldProcessorPerThread:
	DocFieldProcessorPerField:

- DocumentWriter:
RAMBuffer management for CharBlockPool/ByteBlockPool/IntBlockPool
term -> CharBlockPool
docID/freq/prox -> ByteBlockPool
IntBlockPool中保存的是主要用来写入的信息:分别指向docid+freq及prox信息在ByteBlockPool中的偏移量

- SegmentMerge:
	* HashSet<SegmentInfo> mergingSegments = new HashSet<SegmentInfo>(); //保存正在合并的 段,以防止合并期间再次选中被合并。
	* MergePolicy mergePolicy = new LogByteSizeMergePolicy(this);//合并策略,也即选取哪些段来进 行合并。
	* MergeScheduler mergeScheduler = new ConcurrentMergeScheduler();//段合并器,背后有一个 线程负责合并。
	  ConcurrentMergeScheduler.merge(IndexWriter)主要负责进行段的合并。
	* LinkedList<MergePolicy.OneMerge> pendingMerges = new LinkedList<MergePolicy.OneMerge>();//等待被合并的任务
	* Set<MergePolicy.OneMerge> runningMerges = new HashSet<MergePolicy.OneMerge>();//正 在被合并的任务

    * mergeFactor

	* Inverted Info merge:
		SegmentMergeInfo
		SegmentMergeQueue
	* Store Field merge:
		.fnm .fdt .fdx .nrm
		mergeNorms
		merge TermVector
		merge TermDictionary/PostingList

- ScoreAlgrithm:
score(q,d) = coord(q,d)·queryNorm(q)·∑( tf(t in d)·idf(t)^2·t.getBoost()·norm(t,d) ) 
	* t:Term,这里的Term是指包含域信息的Term,也即title:hello和content:hello是不同的Term
	* coord(q,d):一次搜索可能包含多个搜索词,而一篇文档中也可能包含多个搜索词,此项表示,当一篇
	    文档中包含的搜索词越多,则此文档则打分越高。
	* queryNorm(q):计算每个查询条目的方差和,此值并不影响排序,而仅仅使得不同的query之间的分
	    数可以比较。其公式如下:
	* tf(t in d):Term t在文档d中出现的词频
	* idf(t):Term t在几篇文档中出现过
	* norm(t, d):标准化因子,它包括三个参数:
		- Document boost:此值越大,说明此文档越重要。
		- Field boost:此域越大,说明此域越重要。
		- lengthNorm(field) = (1.0 / Math.sqrt(numTerms)):一个域中包含的Term总数越多,也即
		       文档越长,此值越小,文档越短,此值越大。
	* 各类Boost值
		- t.getBoost():查询语句中每个词的权重,可以在查询中设定某个词更加重要,common^4 hello
		- d.getBoost():文档权重,在索引阶段写入nrm文件,表明某些文档比其他文档更重要。 
		- f.getBoost():域的权重,在索引阶段写入nrm文件,表明某些域比其他的域更重要。

	Document Boost和Field Boost影响的是norm(t, d),
	其公式如下: norm(t,d) = doc.getBoost() · lengthNorm(field) · ∏f.getBoost()
	￼
	field f in d named as t
	它包括三个参数:
	• Document boost:此值越大,说明此文档越重要。
	• Field boost:此域越大,说明此域越重要。
	• lengthNorm(field) = (1.0 / Math.sqrt(numTerms)):一个域中包含的Term总数越多,也即文档越
	长,此值越小,文档越短,此值越大。 其中第三个参数可以在自己的Similarity中影响打分,下面会论述。

	* Customize Similarity.lengthNorm / Document Score Customization
	继承并实现自己的Similarity
	Similariy是计算Lucene打分的最主要的类,实现其中的很多借口可以干预打分的过程。 (1) float computeNorm(String field, FieldInvertState state)
	(2) float lengthNorm(String fieldName, int numTokens)
	(3) float queryNorm(float sumOfSquaredWeights)
	(4) float tf(float freq)
	(5) float idf(int docFreq, int numDocs)
	(6) float coord(int overlap, int maxOverlap)
	(7) float scorePayload(int docId, String fieldName, int start, int end, byte [] payload, int offset, int length)
	它们分别影响Lucene打分计算的如下部分:
	score(q,d) = (6)coord(q,d) · (3)queryNorm(q) · ∑( (4)tf(t in d) · (5)idf(t)2 · t.getBoost() · (1)norm(t,d) ) 
	t in q
	norm(t,d) = doc.getBoost() · (2)lengthNorm(field) · ∏f.getBoost() 
	field f in d named as t

	计算Levenshtein distance:edit distance,对于两个字符串,从一个转换成为另一个所需 要的最少基本操作(添加,删除,替换)数。

- Payload
Payload信息就是存储在倒排表中的,同文档号一起存放,多用于存储与每篇文档相关的一些信息。当然这部分 信息也可以存储域里(stored Field),两者从功能上基本是一样的,然而当要存储的信息很多的时候,存放在倒 排表里,利用跳跃表,有利于大大提高搜索速度。


#### Lucene Search

- Search processing:
1. IndexReader将磁盘上的索引信息读入到内存,INDEX_DIR就是索引文件存放的位置。 
   创建IndexSearcher准备进行搜索。
2. 用户输入查询语句   
3. 创建Analyer用来对查询语句进行词法分析和语言处理。
4. 创建QueryParser用来对查询语句进行语法分析。
5. QueryParser调用parser进行语法分析,形成查询语法树,放到Query中。
6. IndexSearcher调用search对查询语法树Query进行搜索
   构造Weight对象树,用于计算词的权重Term Weight,也即计算打分公式中与仅与搜索语句相关与文档无关的部分(红色部分)。
   构造Scorer对象树,用于计算打分(TermScorer.score())。
   在构造Scorer对象树的过程中,其叶子节点的TermScorer会将词典和倒排表从索引中读出来。
   构造SumScorer对象树,其是为了方便合并倒排表对Scorer对象树的从新组织,它的叶子节点仍为 TermScorer,包含词典和倒排表。此步将倒排表合并后得到结果文档集,并对结果文档计算打分公式 中的蓝色部分。打分公式中的求和符合,并非简单的相加,而是根据子查询倒排表的合并方式(与或非) 来对子查询的打分求和,计算出父查询的打分。
7. 将收集的结果集合TopScoreDocCollector及打分返回给用户。

- IndexReader:
	Find out segment_N file
	snapshot

- IndexSearcher:
	IndexSearcher searcher = new IndexSearcher(reader);

- QueryParser(Query语法树):
 	BooleanQuery
 	PrefixQuery
 	TermQuery
 	FuzzyQuery
 	MultiTermQuery

 	Query Object Specification:
	• BooleanQuery即所有的子语句按照布尔关系合并
	◦ +也即MUST表示必须满足的语句
	◦ SHOULD表示可以满足的,minNrShouldMatch表示在SHOULD中必须满足的最小语句个数,
	默认是0,也即既然是SHOULD,也即或的关系,可以一个也不满足(当然没有MUST的时候除
	外)。
	◦ -也即MUST_NOT表示必须不能满足的语句
	• 树的叶子节点中:
	◦ 最基本的是TermQuery,也即表示一个词
	◦ 当然也可以是PrefixQuery和FuzzyQuery,这些查询语句由于特殊的语法,可能对应的不是一
	个词,而是多个词,因而他们都有rewriteMethod对象指向MultiTermQuery的Inner Class, 表示对应多个词,在查询过程中会得到特殊处理。

- Search API
TopDocs docs = searcher.search(query, 50);
• 创建weight树,计算term weight
//重写Query对象树
Query query = searcher.rewrite(this);
//创建Weight对象树
Weight weight = query.createWeight(searcher);
//计算Term Weight分数
idf(t)=1+log(numDocs/(docFreq+1))
float sum = weight.sumOfSquaredWeights();
float norm = getSimilarity(searcher).queryNorm(sum); weight.normalize(norm);

- Score Generate

ConstantScoreAutoRewrite.rewrite
• 创建scorer及SumScorer树,为合并倒排表做准备
• 用SumScorer进行倒排表合并
• 收集文档结果集合及计算打分

ConstantScoreQuery.createWeight(Searcher) 
sumOfSquaredWeights
queryNorm

得到了Scorer对象树以及SumScorer对象树
Scorer scorer = weight.scorer(subReaders[i], !collector.acceptsDocsOutOfOrder(), true);
if (scorer != null) {
￼￼//(d)合并倒排表,(e)收集文档号
	scorer.score(collector); 
}

倒排表的合并以及打分计算

收集文档结果集合及计算打分
TopScoreDocCollector collector = TopScoreDocCollector.create(nDocs, !weight.scoresDocsOutOfOrder());
search(weight, filter, collector); 
return collector.topDocs();

Lucene如何在搜索阶段读取索引信息
	读取词典信息
	读取倒排表信息


#### Lucene Query Language

BooleanQuery,FuzzyQuery, MatchAllDocsQuery,MultiTermQuery,MultiPhraseQuery,PhraseQuery,PrefixQuery, TermRangeQuery,TermQuery,WildcardQuery

JavaCC

QueryParser
	声明QueryParser类
	声明词法分析器
	声明语法分析器

Advanced Query
• BoostingQuery
• CustomScoreQuery
• MoreLikeThisQuery
• MultiTermQuery
	◦ NumericRangeQuery<T>
	◦ TermRangeQuery
• SpanQuery 位置查询
	◦ FieldMaskingSpanQuery 
	◦ SpanFirstQuery
	◦ SpanNearQuery
		▪ PayloadNearQuery 
	◦ SpanNotQuery
	◦ SpanOrQuery
	◦ SpanRegexQuery 
	- FieldMaskingSpanQuery
	◦ SpanTermQuery
		▪ PayloadTermQuery
• FilteredQuery
	Query/Filter
	DuplicateFilter
	FieldCacheRangeFilter<T>及FieldCacheTermsFilter
	MultiTermQueryWrapperFilter<Q>
	QueryWrapperFilter
	SpanFilter/CachingSpanFilter

#### Lucene Analyzer
	• TokenStream tokenStream(String fieldName, Reader reader);
	• TokenStream reusableTokenStream(String fieldName, Reader reader) ;

- TokenStream
	• boolean incrementToken()用于得到下一个Token。
	• public void reset() 使得此TokenStrean可以重新开始返回各个分词。

	NumericTokenStream
	SingleTokenTokenStream
	Tokenizer->TokenStream
		• CharTokenizer
			◦ LetterTokenizer
			▪ LowerCaseTokenizer 
			◦ WhitespaceTokenizer
		• ChineseTokenizer
		• CJKTokenizer
		• EdgeNGramTokenizer 
		• KeywordTokenizer
		• NGramTokenizer
		• SentenceTokenizer
		• StandardTokenizer

- TokenFilter->TokenStream
	public abstract class TokenFilter extends TokenStream { protected final TokenStream input;
	protected TokenFilter(TokenStream input) {
	super(input);
	this.input = input; }
	}

	PorterStemFilter

- Anlayzer = (Tokenizer + TokenFilter) -> TokenStream

ChineseAnalyzer
CJKAnalyzer
PorterStemAnalyzer
SmartChineseAnalyzer
SnowballAnalyzer

- Lucene Standard Tokenizer
StandardTokenizerImpl.jflex
jflex也是一个词法及语法分析器的生成器,它主要包括三部分,由%%分隔:
• 用户代码部分:多为package或者import • 选项及词法声明
• 语法规则声明

StandardTokenizer
StandardFilter
StandardAnalyzer

- PerFieldAnalyzerWrapper

#### Lucene Transactions

所谓事务性,本多指数据库的属性,包括ACID四个基本要素:原子性(Atomicity)、一致性 (Consistency)、隔离性(Isolation)、持久性(Durability)。
我们这里主要讨论隔离性,Lucene的IndexReader和IndexWriter具有隔离性。
• 当IndexReader.open一个索引的时候,相对于给当前索引进行了一次snapshot,此后的任何修改 都不会被看到。
• 仅当IndexReader.close一个索引后,才有可能看到从上次打开后对索引的修改。
• 当IndexWriter没有调用Commit的时候,其修改的内容是不能够被看到的,哪怕IndexReader被重新
打开。
• 欲使最新的修改被看到,一方面IndexWriter需要commit,一方面IndexReader重新打开。

.由于lucene Transaction特性，原生不支持实时查询。需要借助Cache保存Index信息


### FullText Search Function Analysis

### xDB lucene Multi-path Index Search Design

xDB represents the tokens by a list of posting and each posting has one or more keys and a position value of the key in the node. 
All type keys will be converted into strings eventually because Lucene index only can store string. 

Here are some samples of path value index definitions.
/dmftdoc[content<FULL_TEXT::GET_ALL_TEXT>] defines one full text key on path /dmftdoc/content and will be used when a query like /dmftdoc/content[. ftcontains ‘value’]. The element value at path /dmftdoc/content will be first tokenized and sent to Lucene Plug-in. 

Explicit index / Implicit composite key index 

Overall, LMPI system is divided into two major layers.
- Transaction layer, including transaction management and cached data inside transaction.
- Lucene MultiPath Index layer, which encapsulates the native Lucene Indexes (SubIndexes), provides index view to transaction layer.

Only one read-write transaction can update one LMPI and this concurrent access is controlled in xDB by a read-write lock. In another word, LMPI is designed as a non-concurrent index. It follows the lucene instruction.
Here is Lucene’s concurrency rules are simple but should be strictly followed:
- Any number of read-only operations may be executed concurrently. 
- Any number of read-only operations may be executed while an index is being modified.
- Only a single index-modifying operation may execute at a time.
The transaction has a snapshot of a visible part of the index

IndexReader works like a snapshot and the entire query on this index in this transaction will search this snapshot. 
There is a private black list to record the deleted document’s xDB node ID.
Before committing, all data is kept private to this transaction.The commit operation does not flush any pages and only transaction log records will be flushed on disk.

Each read-write transaction creates two data structures, one Lucene SubIndex and one black list. 
There is only one concurrent index for all blacklists of LMPI.

SubIndex merging
The merging policy will strongly impact the overall system performance.

The sub-indexes are classified into two categories.
1.	Final indexes(Final merge), which are created by initialization
2.	Non-final indexes(Clean merge), which are created by a transaction committing or merging non final indexes.
Every transaction creates a separate sub-indexes which are sorted as a list by ascending order of the transaction least LSN. This order reflects the sequence of transactions because the LMPI is a non-concurrent index. 

The sub-index lists as well as in-memory cache are concurrently accessed by multiple threads and some operations like index snapshot view construction need iterate all sub-indexes. 

In order to support cross-index merging of LMPI, each compression mapping structure (a namebase) is assigned a unique identifier (UUID).

Lucene multipath indexes list
Two Sub-indexes can be merged if the following criteria is met.
1.	Two sub-indexes have continuous minimum LSN or no other sub-index has the minimum LSN in the middle.
2.	There are some tuning parameters for merging to reduce the performance impact of merging.

xDB Lucene Index Limitation
- xDB xml document convert to Lucene document object
- lucene index process performance
- lucene sub-merge performance (non-final merge/final merge)


### ElasticSearch & MongoDB Search Design

### Limitation

### Conclusion
