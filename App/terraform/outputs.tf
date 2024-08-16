output "resource_group_name" {
  value = azurerm_resource_group.flask_app_rg.name
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.flask_app_aks.kube_config
  sensitive = true
}

