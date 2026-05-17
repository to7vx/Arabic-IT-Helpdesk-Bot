# Arabic NLP Encoder Models

**Researched:** 2026-05  
**Decision affected:** [ADR-0003 Arabic NLP stack](../decisions/0003-arabic-nlp-stack.md)

## Question

Which transformer encoder should we use as the backbone for Arabic ticket classification, NER, and sentence representation in the helpdesk pipeline?

## Candidates

| Model | Params | Pretraining focus | Notes |
|---|---|---|---|
| **AraBERT v2** (`aubmindlab/bert-base-arabertv02`) | 135M | MSA + news + Wikipedia | Most widely adopted Arabic BERT |
| **MARBERT** (`UBC-NLP/MARBERT`) | 163M | 1B tweets, dialect-heavy | Strong on social / dialectal text |
| **CAMeLBERT-MSA / -DA / -Mix** (`CAMeL-Lab/...`) | 110M | Curated MSA, Dialectal, or mixed | Variants per dialect coverage |
| **AraT5** | 220M+ | Seq2seq | Use only when generative head needed |

## Empirical signal

* **Crime text classification:** MARBERT > AraBERT, F1 = 0.84 (MARBERT) vs. lower for AraBERT and multilingual baselines (Assessing BERT-based models for Arabic, PMC, 2025).
* **Dialect classification:** MARBERT best at 65% accuracy / 64% F1; AraBERT 63%; CAMeLBERT and multilingual-E5 both ~60% (arxiv:2506.19753).
* **Fake news (MSA):** CAMeLBERT-MSA tends to lead, attributed to clean MSA pretraining (Nature Sci. Rep., 2026 article).
* **General review** (Adnan Masood, 2024–2026) confirms AraBERT/MARBERT/CAMeLBERT as the three "default" backbones; specialized domain corpora justify CAMeLBERT variants.

## Recommendation

* Default backbone: **MARBERT** for ticket categorization and sentiment — IT-helpdesk text contains significant dialect and "Arabizi-adjacent" noise, where MARBERT consistently outperforms.
* Secondary backbone: **CAMeLBERT-MSA** for "formal" KB-article tasks (longer, edited prose).
* Fine-tune both, ensemble at inference, pick by language/dialect detector confidence.
* Export production models to **ONNX**, INT8-quantized, target < 100 MB on disk.

## Sources

- Adnan Masood, *A Comprehensive Review of Arabic NLP — From Calligraphy to Transformers* (Medium): https://medium.com/@adnanmasood/a-comprehensive-review-of-arabic-nlp-from-calligraphy-to-transformers-9617e694253f
- *Assessing BERT-based models for Arabic and low-resource languages in crime text classification* (PMC12453752): https://pmc.ncbi.nlm.nih.gov/articles/PMC12453752/
- *Arabic Dialect Classification using RNNs, Transformers, and Large Language Models* (arXiv:2506.19753): https://arxiv.org/html/2506.19753v2
- *BERT Models for Arabic Text Classification: A Systematic Review* (MDPI Applied Sciences 12/11): https://www.mdpi.com/2076-3417/12/11/5720
- Awesome Arabic NLP: https://github.com/Curated-Awesome-Lists/awesome-arabic-nlp
