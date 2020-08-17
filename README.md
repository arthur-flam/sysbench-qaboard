# Disk benchmarking

## What does it do?
This project is a QA-Board wrapper around [sysbench](https://github.com/akopytov/sysbench):

```bash
sysbench fileio prepare
sysbench fileio --file-test-mode=rndrw run --histogram
```

It will show a latency histogram and lots of relevant metrics qualifying throughput etc.

> Don't draw conclusions from the results!
>
> For scientific measurements, we should repeat experiments, worry about and flush OS caches, etc.

References:
- [Sysbench man](https://manpages.debian.org/testing/sysbench/sysbench.1.en.html)
- [Sysbench usage](https://wiki.gentoo.org/wiki/Sysbench)
- [It can get tricky fast](https://www.alibabacloud.com/blog/testing-io-performance-with-sysbench_594709)

## Requirements
```bash
sudo apt install sysbench
```

## How to run
To measure the performance of a network drive
```bash
mkdir /algo/qa_db/benchmark
qa --share run --input /algo/qa_db/benchmark
```

To run on multiple locations, edit *qa/batches.yaml* and:

```bash
qa --share batch benchmark
```

When you are done, cleanup temporary files:

```bash
rm -rf /algo/qa_db/benchmark/*
```


