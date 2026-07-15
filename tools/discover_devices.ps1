[CmdletBinding()]
param()

$ErrorActionPreference = "SilentlyContinue"

$adapters = Get-NetAdapter -IncludeHidden |
    Where-Object {
        $_.InterfaceDescription -match "USB|RNDIS|Remote NDIS|Ethernet Gadget|Maix|Sipeed" -or
        $_.Name -match "USB|Maix|Sipeed"
    } |
    ForEach-Object {
        $adapter = $_
        $addresses = Get-NetIPAddress -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4 |
            Select-Object -ExpandProperty IPAddress
        [pscustomobject]@{
            Name = $adapter.Name
            Description = $adapter.InterfaceDescription
            Status = [string]$adapter.Status
            MacAddress = $adapter.MacAddress
            LinkSpeed = [string]$adapter.LinkSpeed
            InterfaceIndex = $adapter.ifIndex
            IPv4 = @($addresses)
        }
    }

$serialPorts = Get-CimInstance Win32_SerialPort |
    ForEach-Object {
        [pscustomobject]@{
            DeviceId = $_.DeviceID
            Name = $_.Name
            Description = $_.Description
            PnpDeviceId = $_.PNPDeviceID
        }
    }

[pscustomobject]@{
    Timestamp = (Get-Date).ToString("o")
    UsbNetworkCandidates = @($adapters)
    SerialPortCandidates = @($serialPorts)
    Safety = "Discovery only. Confirm 3.3V TTL and common ground before UART wiring."
} | ConvertTo-Json -Depth 6
