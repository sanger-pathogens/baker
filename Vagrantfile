Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "8192"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update -y -qq && apt-get install -y -qq \
      git \
      python3 \
      python3-pip

    # default python packages
    pip3 install virtualenv

  SHELL
end
