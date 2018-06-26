!#/bin/bash
useradd ansible -s /bin/bash ; mkdir -p /home/ansible/.ssh/ ; chmod 0700 /home/ansible/.ssh/ ; chown -R ansible:ansible /home/ansible/ ; echo "ansible ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
