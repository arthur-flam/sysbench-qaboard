# sysbench & QA-Board
This project is a QA-Board wrapper around [sysbench](https://github.com/akopytov/sysbench)'s **fileio** benchmark suit:

## Requirements
```bash
# with debian
sudo apt install sysbench

# with other systems
# https://github.com/akopytov/sysbench
```

## Usage
Edit *qa/batches.yaml* to configure the benchmark. For instance, for a `fileio` benchmark:

```yaml
benchark-fileio:
  inputs:
  - /some/disk
  # https://github.com/akopytov/sysbench#general-syntax
  configs:
    # the test will prepare/run/clean
  - testname: fileio
    prepare: true  # default is false!
    clean: true    # default is false!
    # options will be forwared: sysbench [testname] run --flag/--param-name value
    file-test-mode: rndrw
    histogram: true
```

Then start with

```bash
qa batch benchark-fileio
```

To start a `cpu` benchmark:

```yaml
benchark-cpu:
  inputs:
  - /proc/cpuinfo
  configs:
  - testname: cpu
```

## References:
- [Sysbench man](https://manpages.debian.org/testing/sysbench/sysbench.1.en.html)
- [Sysbench usage](https://wiki.gentoo.org/wiki/Sysbench)
- [It can get tricky fast](https://www.alibabacloud.com/blog/testing-io-performance-with-sysbench_594709)

## TODO
- Add relevant metrics/graphs for each test suit
  * [x] `fileio`
  * [ ] `oltp_*.lua`
  * [ ] `cpu`
  * [ ] `memory`
  * [ ] `threads`
  * [ ] `mutex`
