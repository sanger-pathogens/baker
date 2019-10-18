Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "8192"
  end

  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive

    apt-get update -qq -y && apt-get upgrade -qq -y

    # Dependencies for singularity and python
    apt-get update -qq -y && apt-get install -qq -y \
      build-essential \
      libssl-dev \
      uuid-dev \
      libgpgme11-dev \
      squashfs-tools \
      libseccomp-dev \
      wget \
      pkg-config \
      git \
      python3 \
      python3-pip \
      software-properties-common \
      cryptsetup-bin \
      uidmap

    # Go
    add-apt-repository ppa:longsleep/golang-backports && \
      apt-get update -qq -y && \
      apt-get install golang-go  -qq -y

    # Singularity
    export SINGULARITY_VERSION=3.4.0
    mkdir /tmp/singularity
    cd /tmp/singularity
    wget -q https://github.com/sylabs/singularity/releases/download/v${SINGULARITY_VERSION}/singularity-${SINGULARITY_VERSION}.tar.gz
    tar -xf singularity-${SINGULARITY_VERSION}.tar.gz
    cd singularity
    ./mconfig
    make -C builddir
    make -C builddir install
    cd /tmp
    rm -rf /tmp/singularity

    # default python packages
    pip3 install virtualenv

  SHELL
end
