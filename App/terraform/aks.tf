resource "azurerm_kubernetes_cluster" "flask_app_aks" {
  name                = "flaskAppAKSCluster"
  location            = azurerm_resource_group.flask_app_rg.location
  resource_group_name = azurerm_resource_group.flask_app_rg.name
  dns_prefix          = "flaskappakscluster"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_DS2_v2"
    vnet_subnet_id = azurerm_subnet.example.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    network_policy    = "azure"
    service_cidr      = "10.1.0.0/16"  # Specify a non-conflicting CIDR
    dns_service_ip    = "10.1.0.10"
  }

#   role_based_access_control {
#     enabled = true
#   }

#   addon_profile {
#     oms_agent {
#       enabled                    = true
#       log_analytics_workspace_id = azurerm_log_analytics_workspace.example.id
#     }
#   }
}
