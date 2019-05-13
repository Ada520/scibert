"""

Alternative to `exp.sh` script because it doesn't seem to run properly on UNIX machines

"""

import subprocess
import plac
import sys
import subprocess

@plac.annotations(
        desc=("description", "positional", None, str),
        not_dry_run=("actually run it ?", "flag", "not_dry_run", bool),
)
def main(desc: str, not_dry_run: bool = False):

    dataset_sizes = {
                    'NCBI-disease': 5424,
                    'bc5cdr': 4942,
                    'JNLPBA': 18607,
                    'sciie': 2211,
                    'chemprot': 4169,
                    'citation_intent': 1688,
                    'mag': 84000,
                    'rct-20k': 180040,
                    'sciie-relation-extraction': 3219,
                    'sci-cite': 7320,
                    'ebmnlp': 38124,
                    'genia': 14326,
                    }

    for dataset in [
                    # 'NCBI-disease',
                    # 'bc5cdr',
                    # 'JNLPBA',
                    # 'sciie',
                    'chemprot',
                    'citation_intent',
                    'mag',
                    'rct-20k',
                    'sciie-relation-extraction',
                    'sci-cite',
                    # 'ebmnlp',
                    # 'genia',
                ]:
        for seed in [
                    # 15370,
                    # 15570,
                    # 15680,
                    # 15780,
                    # 15210,
                    # 16210,
                    # 16310,
                    # 16410,
                    # 18210,
                    # 18310,
                    # 18410,
                    # 18510,
                    18610
                    ]:

            pytorch_seed = seed // 10
            numpy_seed = pytorch_seed // 10

            for model in [
                        # 'bertbase_basevocab_uncased',
                        # 'bertbase_basevocab_cased',
                        # 'biobert_pmc_basevocab_cased',
                        # 'biobert_pubmed_pmc_basevocab_cased',
                        # 'biobert_pubmed_basevocab_cased',
                        # 'scibert_basevocab_uncased_512',
                        # 'scibert_basevocab_cased_512',
                        'scibert_scivocab_uncased_512',
                        # 'scibert_scivocab_cased_512',
                        ]:

                for with_finetuning in ['_finetune', ]: # , '']:

                    if dataset in ['NCBI-disease', 'bc5cdr', 'JNLPBA', 'sciie']:
                        task = 'ner'
                    elif dataset in ['chemprot', 'citation_intent', 'mag', 'rct-20k', 'sciie-relation-extraction', 'sci-cite']:
                        task = 'text_classification'
                    elif dataset in ['ebmnlp']:
                        task = 'pico'
                    elif dataset in ['genia']:
                        task = 'parsing'
                    else:
                        assert False

                    dataset_size = dataset_sizes[dataset]

                    # determine casing based on model
                    if 'uncased' in model:
                        is_lowercase = 'true'
                        vocab_file = 'uncased'
                    else:
                        is_lowercase = 'false'
                        vocab_file = 'cased'

                    # determine vocab file based on model
                    if 'basevocab' in model:
                        vocab_file = 'basevocab_' + vocab_file
                    else:
                        vocab_file = 'scivocab_' + vocab_file

                    # config file
                    config_file = f'allennlp_config/{task}{with_finetuning}.json'

                    # bert files
                    bert_vocab = f'/bert_vocab/{vocab_file}.vocab'
                    bert_weights = f'/bert_weights/{model}.tar.gz'

                    # data files
                    train_path = f'data/{task}/{dataset}/train.txt'
                    dev_path = f'data/{task}/{dataset}/dev.txt'
                    test_path = f'data/{task}/{dataset}/test.txt'

                    print(task, dataset, seed, bert_weights, bert_vocab, train_path)
                    cmd = ' '.join(['python', 'scripts/run_with_beaker.py',
                        f'{config_file}',
                        '--source ds_dpsaxi4ltpw9:/bert_vocab/',
                        '--source ds_jda1d19zqy6z:/bert_weights/',
                        '--include-package scibert',
                        '--env CUDA_DEVICE=0',
                        f'--env DATASET_SIZE={dataset_size}',
                        f'--env BERT_VOCAB={bert_vocab}',
                        f'--env BERT_WEIGHTS={bert_weights}',
                        f'--env TRAIN_PATH={train_path}',
                        f'--env DEV_PATH={dev_path}',
                        f'--env TEST_PATH={test_path}',
                        f'--env IS_LOWERCASE={is_lowercase}',
                        f'--env SEED={seed}',
                        f'--env PYTORCH_SEED={pytorch_seed}',
                        f'--env NUMPY_SEED={numpy_seed}'])
                    if not_dry_run:
                        completed = subprocess.run(cmd, shell=True)
                        print(f'returncode: {completed.returncode}')

plac.call(main, sys.argv[1:])