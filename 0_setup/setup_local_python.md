# PC上でのPython環境セットアップ

自身のPC上にPythonの実行環境を用意する場合は，[Pipenv](https://pipenv-ja.readthedocs.io/ja/translate-ja/)と[pyenv](https://github.com/pyenv/pyenv)の組合せをおすすめします[^1]．

Pythonを用いた開発ではほぼ間違いなく`pip`コマンドを用いて既存のパッケージを利用することになりますが，最近のOSでは[PEP 668](https://peps.python.org/pep-0668/)の影響によりOSデフォルトのPython環境に直接パッケージをインストールできなくなりました．そのため，`venv`モジュールなどを利用してPython上に仮想環境を作る必要があるのですが，直接`venv`を使うよりも，Pipenvなど便利な機能がまとめられたパッケージを利用する方が管理が簡便です．

また，実際の開発ではプロジェクト毎に別のPython環境を用意する（e.g., 機械学習用のPython環境とコンピュータ科学実験用のPython環境）ことがありますが，その際にベースとなるPythonのバージョンが異なる（e.g., 片方は3.12系を使用しているが他方は3.9系を使っている）場合があります．このような場合に，好きなバージョンのPythonをユーザ空間（i.e., `~/.pyenv`以下）にインストールするためのソフトウェアが`pyenv`です．上記のPipenvと組み合わせることで様々なPC上で統一された実行環境を容易に構築できるようになります．

以下，機械学習の演習を実施するために最低限必要な環境構築の手順を述べます．実際にはここから+αすることで色々と便利になっていくのですが，そちらについては各々調べてみてください[^2]．

## 目次 <!-- omit in toc -->

- [Pipenv/pyenvのインストール](#pipenvpyenvのインストール)
    - [Windows 11の場合](#windows-11の場合)
        - [WSLの導入](#wslの導入)
        - [pyenvのインストール](#pyenvのインストール)
        - [Pipenvのインストール](#pipenvのインストール)
    - [macOSの場合](#macosの場合)
- [演習環境の構築](#演習環境の構築)
    - [Pipfileを使用する場合](#pipfileを使用する場合)
    - [Pipfileを使用しない場合](#pipfileを使用しない場合)

## Pipenv/pyenvのインストール

WindowsかmaxOSかでインストール方法が異なるため，以下ではそれぞれ説明します．他のOSを使用している場合は[pyenvの公式ドキュメント](https://github.com/pyenv/pyenv#installation)を参照してください（Ubuntuの場合はWindowsの場合とほぼ同様でOKです）．

以下，別途明記しない限り全てのコマンドは各OS標準のターミナル（WindowsでWSLインストール後はUbuntuのターミナル）で実行します．

### Windows 11の場合

#### WSLの導入

Windows 11上で直接Pythonを動かすこともできますが，管理が煩雑で個人的におすすめできないため，以下では[Windows Subsystem for Linux（WSL）](https://docs.microsoft.com/ja-jp/windows/wsl/about)の利用を前提に説明します．WSLはその名の通りWindows上のサブシステムとしてLinuxを動作させる機能で，これを用いることで例えば[Ubuntu](https://jp.ubuntu.com/)をWindows上で実行できます（仮想マシンを利用したことがある人は，ほぼそれと同じ仕組みだと理解してもらえればOKです）．詳細なインストール方法は[Microsoft公式のドキュメント](https://docs.microsoft.com/ja-jp/windows/wsl/install)にあるため，基本的にはそちらを参照してください．以下はインストール手順の抜粋です．

まず，以下のコマンドを**管理者権限付きの**PowerShellで実行してWSLをインストールしてください．しばらく待つとWSLのインストールが終わった旨のメッセージが出力されるため，PCを再起動してください．起動後に自動で最新版のUbuntuが立ち上がるため，ユーザ名とパスワードを設定すればUbuntuが使用できる状態になります．

```PowerShell
# @PowerShell
wsl --install
```

`pipenv`についてはUbuntuのパッケージマネージャ経由でもインストールできますが，バージョンが古くなりがちのため`pip`経由でインストールすることをおすすめします．そのため，以下ではまず`pyenv`からインストールしていきます．

#### pyenvのインストール

`pyenv`のインストールには公式のインストーラを使用する必要があるため，まずビルドに必要なパッケージをインストールします．

<!-- cSpell:disable -->
```bash
# @Terminal on Ubuntu
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```
<!-- cSpell:enable -->

その後，提供されているインストーラーを用いて`pyenv`をインストールします．

```bash
# @Terminal on Ubuntu
curl https://pyenv.run | bash
```

最後に，`pyenv`を動作させるための環境変数を書き出したら準備完了です．以下は環境変数の設定例ですが，シェルとして`bash`を使用している想定になります．なお，これらのコマンドを実行したら一度ターミナルを立ち上げなおして（i.e., 一度閉じてから再度開いて）ください．

```bash
# @Terminal on Ubuntu
cat << 'EOF' >> ${HOME}/.bashrc

# enable pyenv
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF
exec $SHELL
```

なお，長い期間利用していると`pyenv`側が古くなりすぎて新しいバージョンのPythonをインストールできなくなります．その際は以下のコマンドで`pyenv`自体を更新してください．

```bash
# @Terminal on Ubuntu
pyenv update
```

#### Pipenvのインストール

Pipenvをインストールする前に，デフォルトで使用するPythonを設定しておきます．以下のコマンドでインストール可能なPythonのバージョンを確認し，適当に好きなバージョンを選んでください．

```bash
# @Terminal on Ubuntu/Mac
pyenv install --list | grep -E '^\s*3.*'
```

ここでは例として，執筆時点でColabで使用されている`3.11.11`をインストールします．

```bash
# @Terminal on Ubuntu/Mac
pyenv install 3.11.11
```

少し待つとインストールが終わるため，デフォルトで使用するPythonのバージョンをインストールした`3.11.11`に設定し，設定が反映されているか確認します．もし以下のコマンドを入力して`python`のバージョンが期待したものでない（i.e., OSデフォルトのPythonの）場合は一度Ubuntuないし端末を起動しなおしてみてください．

```bash
# @Terminal on Ubuntu/Mac
pyenv global 3.11.11
pyenv global
python --version
pip --version
```

デフォルトで使用するPythonが設定できたら，次は`pip`本体を更新します．

```bash
# @Terminal on Ubuntu/Mac
python -m pip install --upgrade pip
```

最後に，`pipenv`をインストールしたら準備は完了です．

```bash
# @Terminal on Ubuntu/Mac
pip install pipenv
```

### macOSの場合

macOSの場合は[Homebrew](https://brew.sh/)を用いて両者共にインストールできます．もしHomebrewをインストールしていない場合は以下のコマンドでインストール可能です．なお，[HomebrewのインストールオプションでXcode Command Line Toolsもインストールできる](https://mac.install.guide/commandlinetools/3.html)ため，一緒にいれておくのをおすすめします．

```bash
# @Terminal
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

`brew`コマンドを使用できる状態になったら，以下のコマンドで`pipenv`および`pyenv`をインストールします．なお，`pip`経由でPipenvをインストールしたい場合はWindows側の説明を参照してください．

```bash
# @Terminal
brew install pipenv pyenv
```

最後に，`pyenv`を動作させるための環境変数を書き出したら準備完了です．以下は環境変数の設定例ですが，シェルとして`zsh`を使用している想定になります．なお，これらのコマンドを実行したら一度ターミナルを立ち上げなおして（i.e., 一度閉じてから再度開いて）ください．

```bash
# @Terminal
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

## 演習環境の構築

演習用のディレクトリとして，以下では`~/workspace/python/ml-exercises`というディレクトリ上で作業すると想定します．

```bash
# @Terminal on Ubuntu/Mac
mkdir -p ~/workspace/python/
git clone https://github.com/baycedar/ml-exercises-sample.git ~/workspace/python/ml-exercises
cd ~/workspace/python/ml-exercises
```

### Pipfileを使用する場合

まず，演習で使用するPython環境をセットアップします．このリポジトリに環境を整えるための`Pipfile`を同梱しているため，以下のコマンドでColabにインストールされているバージョンと揃えた環境を準備できます．なお，対応するバージョンのPythonがインストールされていない場合，まず該当のバージョンが`pyenv`によってインストールされ若干時間がかかるため注意してください．

```bash
# @Terminal on Ubuntu/Mac
pipenv install -d
```

パッケージをインストールした後，以下のコマンドを実行するとブラウザで[Jupyter](https://jupyter.org/)を開くためのURLが`Or copy and paste one of these URLs:`というメッセージに続いて表示されます．ブラウザで該当のページを開いた後はおおよそColabと同じ操作感でPtyhonのプログラミングが可能です．

```bash
# @Terminal on Ubuntu/Mac
pipenv run jupyter notebook --no-browser
```

もしくは，せっかくローカルでPythonを動かせる環境を作ったのであれば[VS Code](https://azure.microsoft.com/ja-jp/products/visual-studio-code/)など適当なIDEを使用してもよいと思います．ここから先は個人の好みによる部分が大きいので，快適なコーディング環境を探して色々と試行錯誤してみてください．

### Pipfileを使用しない場合

以下は`Pipfile`を使用せずに環境を整える例です．使用するPythonのバージョンはある程度新しければなんでもよい[^3]ですが，以下では執筆時点でのColabのPythonバージョンにあわせて`3.11.11`を使用しています．

```bash
# @Terminal on Ubuntu/Mac
pipenv install --python 3.11.11
```

次に，演習で使用するパッケージをインストールします．色々あるのですが，最低以下の4つを入れておけば依存関係で他の使用するパッケージもインストールされます．

```bash
# @Terminal on Ubuntu/Mac
pipenv install jupyter scikit-learn pandas matplotlib
```

[^1]: Pipenvと同等の機能を持つパッケージ管理ツールとして[Poetry](https://python-poetry.org/)というものもあります．いずれを使うかは個人の趣味や所属する組織の方針によると思いますが，ひとまずここではPipenvの使用を前提とします．
[^2]: 希望があってかつ自分の時間もあれば何か追記します．
[^3]: 稀にバージョン違いによって計算結果が異なる（内部関数の挙動が微妙に異なる）ことがあるため，揃えておいた方が安心ではあります．
