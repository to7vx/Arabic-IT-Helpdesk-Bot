# Arabic Tokenization & Morphology

**Researched:** 2026-05  
**Decision affected:** [ADR-0006 Arabic preprocessing pipeline](../decisions/0006-arabic-preprocessing-pipeline.md)

## Question

Which library should perform morphological segmentation, lemmatization, and POS tagging upstream of classification and retrieval?

## Candidates

* **Farasa** (Qatar Computing Research Institute) — fast rank-SVM segmenter trained on the Penn Arabic Treebank, optimized for MSA news.
* **CAMeL Tools** (NYU Abu Dhabi CAMeL Lab) — integrated Python toolkit: morphology, disambiguation, POS, sentiment, NER, dialect ID.
* **Stanza** (Stanford) — multilingual; weaker Arabic-specific coverage.
* **Subword (SentencePiece / BPE)** — used inside transformer models; not a substitute for analyzer when we need lemmas for sparse retrieval.

## Empirical signal

* 2026 multi-corpus evaluation across modern, classical religious, and jurisprudential Arabic: **CAMeL significantly outperforms Farasa across all domains** (J. Open Humanities Data, 10.5334/johd.418).
* Farasa shows steepest accuracy decline as clitic-count grows; CAMeL and ALP remain stable.
* Older work (Alyafeai et al., arXiv:2106.07540) finds that tokenizer choice affects Arabic classification accuracy by several points.

## Recommendation

* **Lemmatization + POS:** CAMeL Tools (`MorphologyDB`, `Disambiguator`).
* **Fast segmentation fallback:** Farasa retained behind a flag for batch jobs that need throughput over accuracy.
* **Transformer input:** the model's own tokenizer (AraBERT v2 / MARBERT WordPiece, BGE-M3 SentencePiece) — never pre-segment before feeding a transformer.
* **Sparse retrieval (BM25):** lemmatize with CAMeL Tools, then BM25 over lemmas.

## Sources

- *Domain Sensitivity in Arabic Morphological Analysis: A Multi-Corpus Evaluation of Farasa, CAMeL, and ALP* (J. Open Humanities Data, 2026): https://openhumanitiesdata.metajnl.com/articles/10.5334/johd.418
- *CAMeL Tools: An Open Source Python Toolkit for Arabic NLP* (LREC 2020): https://aclanthology.org/2020.lrec-1.868v1.pdf
- Farasa paper (Abdelali et al.): https://www.researchgate.net/publication/303989318_Farasa_A_Fast_and_Furious_Segmenter_for_Arabic
- *Evaluating Various Tokenizers for Arabic Text Classification* (arXiv:2106.07540): https://arxiv.org/pdf/2106.07540
