provider "google" {
  credentials = "${file("${var.api-key}")}"
  project = "${var.project}"
  region  = "${var.region}"
  zone    = "${var.zone}"
}

resource "google_compute_firewall" "heartbeat-svc-fw" {
  name = "heartbeat-fw"
  network = "default"

  allow {
    protocol = "tcp"
    ports = ["9070"]
  }

  target_tags = ["heartbeat-svc"]
  source_ranges = ["0.0.0.0/0"]
}


resource "google_compute_instance" "heartbeat_instance" {
  name         = "heartbeat"
  machine_type = "f1-micro"

  tags = ["heartbeat-svc"]

  boot_disk {
    initialize_params {
      image = "ubuntu-minimal-1804-lts"
    }
  }

  network_interface {
      network = "default"
        access_config {
         nat_ip = ""
      }
    }

  provisioner "remote-exec" {
        inline = [
            "sudo apt-get update",
            "sudo mkdir -p /data/app",
        ]

        connection {
            type = "ssh"
            host = "${self.network_interface.0.access_config.0.nat_ip}"
            user = "yevgeny"
            private_key = "${file("${var.ssh-key}")}"
            agent = "false"
        }
    }

  provisioner "local-exec" {
        command = "cd playbook && ansible-playbook -i '${self.network_interface.0.access_config.0.nat_ip},' --private-key ${var.ssh-key} provision.yaml -e 'ansible_python_interpreter=/usr/bin/python3' --become"
    }

  provisioner "local-exec" {
        command =<<EOF
         echo http://${self.network_interface.0.access_config.0.nat_ip}:9070/heartbeat >> heartbeat-endpoints.txt
         echo http://${self.network_interface.0.access_config.0.nat_ip}:9070/report >> heartbeat-endpoints.txt
       EOF
    }
  

}

