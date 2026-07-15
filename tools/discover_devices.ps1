[CmdletBinding()]
param(
    [switch]$ProbeSsh,
    [ValidateRange(100, 5000)]
    [int]$ProbeTimeoutMs = 700
)

$ErrorActionPreference = "Stop"
$errors = [System.Collections.Generic.List[string]]::new()

function Get-ExpectedDeviceIPv4 {
    param(
        [Parameter(Mandatory)]
        [string]$HostIPv4,
        [Parameter(Mandatory)]
        [int]$PrefixLength
    )

    $parsed = $null
    if ($PrefixLength -ne 24 -or -not [System.Net.IPAddress]::TryParse($HostIPv4, [ref]$parsed)) {
        return $null
    }

    $octets = $parsed.GetAddressBytes()
    $octets[3] = 1
    return ($octets -join ".")
}

function Test-TcpPort {
    param(
        [Parameter(Mandatory)]
        [string]$HostName,
        [Parameter(Mandatory)]
        [int]$Port,
        [Parameter(Mandatory)]
        [int]$TimeoutMs
    )

    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $connectTask = $client.ConnectAsync($HostName, $Port)
        return $connectTask.Wait($TimeoutMs) -and $client.Connected
    }
    catch {
        return $false
    }
    finally {
        $client.Dispose()
    }
}

try {
    $adapterCandidates = @(
        Get-NetAdapter -IncludeHidden |
            Where-Object {
                $_.InterfaceDescription -match "USB|RNDIS|Remote NDIS|Ethernet Gadget|Maix|Sipeed|NCM" -or
                $_.Name -match "USB|Maix|Sipeed"
            }
    )
}
catch {
    $adapterCandidates = @()
    $errors.Add("Get-NetAdapter failed: $($_.Exception.Message)")
}

$adapters = foreach ($adapter in $adapterCandidates) {
    try {
        $addresses = @(
            Get-NetIPAddress -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4 |
                ForEach-Object {
                    $expectedDeviceIp = Get-ExpectedDeviceIPv4 -HostIPv4 $_.IPAddress -PrefixLength $_.PrefixLength
                    [pscustomobject]@{
                        HostIPv4 = $_.IPAddress
                        PrefixLength = $_.PrefixLength
                        ExpectedDeviceIPv4 = $expectedDeviceIp
                        SshPort22Open = if ($ProbeSsh -and $expectedDeviceIp) {
                            Test-TcpPort -HostName $expectedDeviceIp -Port 22 -TimeoutMs $ProbeTimeoutMs
                        }
                        else {
                            $null
                        }
                    }
                }
        )
    }
    catch {
        $addresses = @()
        $errors.Add("Get-NetIPAddress failed for interface $($adapter.ifIndex): $($_.Exception.Message)")
    }

    [pscustomobject]@{
        Name = $adapter.Name
        Description = $adapter.InterfaceDescription
        Status = [string]$adapter.Status
        MacAddress = $adapter.MacAddress
        LinkSpeed = [string]$adapter.LinkSpeed
        InterfaceIndex = $adapter.ifIndex
        IPv4 = $addresses
    }
}

try {
    $serialPorts = @(
        Get-CimInstance Win32_SerialPort |
            ForEach-Object {
                [pscustomobject]@{
                    DeviceId = $_.DeviceID
                    Name = $_.Name
                    Description = $_.Description
                    PnpDeviceId = $_.PNPDeviceID
                }
            }
    )
}
catch {
    $serialPorts = @()
    $errors.Add("Win32_SerialPort query failed: $($_.Exception.Message)")
}

$isAdministrator = $false
try {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    $isAdministrator = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}
catch {
    $errors.Add("Administrator check failed: $($_.Exception.Message)")
}

[pscustomobject]@{
    Timestamp = (Get-Date).ToString("o")
    HostName = $env:COMPUTERNAME
    IsAdministrator = $isAdministrator
    ProbeSsh = [bool]$ProbeSsh
    UsbNetworkCandidates = @($adapters)
    SerialPortCandidates = @($serialPorts)
    DiscoveryErrors = @($errors)
    Safety = "Discovery only. Confirm 3.3V TTL and common ground before UART wiring."
} | ConvertTo-Json -Depth 8
