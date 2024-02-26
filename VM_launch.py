subscription_id = "8066e2ea-f264-454b-8423-3c7fb145632f"
resource_group_name = "LWRG1"
location = "eastus"

from azure.identity import AzureCliCredential
credential = AzureCliCredential()

from azure.mgmt.compute import ComputeManagementClient
compute_client = ComputeManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

from azure.mgmt.network import NetworkManagementClient
network_client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

virtual_network_name = "os1-vnet"
subnet_name = "default"

nic_params = {
        "location": location,
        "ip_configurations": [{
            "name": "ipconfig1",
            "subnet": {
                "id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/virtualNetworks/{virtual_network_name}/subnets/{subnet_name}"
            }
        }]
    }

nic = network_client.network_interfaces.begin_create_or_update(
        resource_group_name,
        "myNic123",
        nic_params
    ).result()



vm_name = "myVM123"
username = "vimal"
password = "LWindia@123456"

vm_params = {
        "location": location,
        "hardware_profile": {
            "vm_size": "Standard_DS1_v2"
        },
        "storage_profile": {
            "image_reference": {
                "publisher": "MicrosoftWindowsServer",
                "offer": "WindowsServer",
                "sku": "2019-Datacenter",
                "version": "latest"
            },
            "os_disk": {
                "create_option": "fromImage"
            }
        },
        "os_profile": {
            "computer_name": vm_name,
            "admin_username": username[:20],  # Limiting the username to 20 characters
            "admin_password": password
        },
        "network_profile": {
            "network_interfaces": [{
                "id": nic.id
            }]
        }
    }

async_vm_creation = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name,
        vm_name,
        vm_params
    )

