data "azurerm_client_config" "example" {}

resource "azurerm_key_vault" "example" {
  name                        = "RPcyberseckeyvault"
  location                    = azurerm_resource_group.flask_app_rg.location
  resource_group_name         = azurerm_resource_group.flask_app_rg.name
  tenant_id                   = data.azurerm_client_config.example.tenant_id
  sku_name                    = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.example.tenant_id
    object_id = data.azurerm_client_config.example.object_id

    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete",
      "Purge"
    ]
  }
}

resource "azurerm_key_vault_secret" "acr-acr_username" {
  name         = "acr-username"
  value        = "your-acr-username"
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "acr_password" {
  name         = "acr-password"
  value        = "your-acr-password"
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "aks_resource_group" {
  name         = "aks-resource-group"
  value        = "your-aks-resource-group"
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "aks_cluster_name" {
  name         = "aks-cluster-name"
  value        = "your-aks-cluster-name"
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "azure_subscription_id" {
  name         = "azure-subscription-id"
  value        = "your-azure-subscription-id"
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "azure_client_id" {
  name         = "azure-client-id"
  value        = "your-azure-client-id"
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "azure_secret" {
  name         = "azure-secret"
  value        = "your-azure-secret"
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "azure_tenant_id" {
  name         = "azure-tenant-id"
  value        = "your-azure-tenant-id"

resource "azurerm_key_vault_secret" "example" {
  name         = "mlapp-secret"
  value        = "my-secret-value"
>>>>>>> 195d03141d80a9186ce728d476cfaaea89febba9
  key_vault_id = azurerm_key_vault.example.id
}
