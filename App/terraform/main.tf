terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0" # Ensure you are using a version that supports azurerm_policy_assignment
    }
  }
}

provider "azurerm" {
  features {}
}


resource "azurerm_resource_group" "flask_app_rg" {
  name     = "flaskAppResourceGroup"
  location = "East US"
}

resource "azurerm_log_analytics_workspace" "example" {
  name                = "example-log-analytics"
  location            = azurerm_resource_group.flask_app_rg.location
  resource_group_name = azurerm_resource_group.flask_app_rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_registry" "example" {
  name                = "RPcybersecurityappacr"
  resource_group_name = azurerm_resource_group.flask_app_rg.name
  location            = azurerm_resource_group.flask_app_rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_virtual_network" "example" {
  name                = "RPcybersecurity-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.flask_app_rg.location
  resource_group_name = azurerm_resource_group.flask_app_rg.name
}

resource "azurerm_subnet" "example" {
  name                 = "example-subnet"
  resource_group_name  = azurerm_resource_group.flask_app_rg.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.0/24"]
}
