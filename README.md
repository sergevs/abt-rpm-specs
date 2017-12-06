# abt-rpm-specs
The repository to store required for [**abt**](https://github.com/sergevs/abt) files to build rpm packages for various applications.

# Overview
Please setup build environment according to [abt getting started](https://github.com/sergevs/abt#getting-started)

Currently implemented builds
  * [Yandex clickhouse](https://github.com/yandex/ClickHouse) for Centos 7
  as far only 1.1.54304 version tested. Next stable v1.1.54310 version can't be build due to [issue](https://github.com/yandex/ClickHouse/issues/1461). Example command to build:
  ```
  abt.docker sergevs42/centos7.x86_64-abt -v 1.1.54304 -b trunk -c clickhouse.abt sergevs/abt-rpm-specs
  ```

   

