# Disk benchmarking

## What does it do?
This project is a QA-Board wrapper around:

```bash
sysbench fileio prepare
sysbench fileio --file-test-mode=rndrw run --histogram
```

It will show a latency histogram and lots of relevant metrics qualifying throughput etc.

> For scientific results, we should repeat experiments, flush OS caches, etc.

## Requirements

```bash
sudo apt install sysbench
```

## How to run

```bash
qa --share run --input /algo/qa_db/benchmark
qa --share batch benchmark

# cleanup tmp files...
rm -rf /algo/qa_db/benchmark/*
```


