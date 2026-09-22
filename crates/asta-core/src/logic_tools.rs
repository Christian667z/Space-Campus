use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConversionResult {
    pub input: String,
    pub decimal: Option<i64>,
    pub binary: Option<String>,
    pub octal: Option<String>,
    pub hexadecimal: Option<String>,
    pub ascii: Option<String>,
    pub error: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SubnetResult {
    pub ip: String,
    pub cidr: u8,
    pub netmask: String,
    pub network_address: String,
    pub broadcast_address: String,
    pub first_host: String,
    pub last_host: String,
    pub total_hosts: u64,
    pub usable_hosts: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BooleanLaw {
    pub name: String,
    pub expression: String,
    pub description: String,
}

/// Convertit un nombre sous n'importe quelle base usuelle (Dec, Bin, Hex, Oct)
pub fn convert_all(input_str: &str) -> ConversionResult {
    let raw = input_str.trim();
    if raw.is_empty() {
        return ConversionResult {
            input: String::new(),
            decimal: None,
            binary: None,
            octal: None,
            hexadecimal: None,
            ascii: None,
            error: Some("Entrée vide".to_string()),
        };
    }

    let parsed_val: Option<i64> = if raw.starts_with("0b") || raw.starts_with("0B") {
        i64::from_str_radix(&raw[2..], 2).ok()
    } else if raw.starts_with("0x") || raw.starts_with("0X") {
        i64::from_str_radix(&raw[2..], 16).ok()
    } else if raw.starts_with("0o") || raw.starts_with("0O") {
        i64::from_str_radix(&raw[2..], 8).ok()
    } else if let Ok(val) = raw.parse::<i64>() {
        Some(val)
    } else if let Ok(val) = i64::from_str_radix(raw, 16) {
        Some(val)
    } else {
        None
    };

    match parsed_val {
        Some(val) => {
            let ascii_rep = if val >= 32 && val <= 126 {
                Some((val as u8 as char).to_string())
            } else {
                None
            };

            ConversionResult {
                input: raw.to_string(),
                decimal: Some(val),
                binary: Some(format!("{:b}", val)),
                octal: Some(format!("{:o}", val)),
                hexadecimal: Some(format!("{:X}", val)),
                ascii: ascii_rep,
                error: None,
            }
        }
        None => ConversionResult {
            input: raw.to_string(),
            decimal: None,
            binary: None,
            octal: None,
            hexadecimal: None,
            ascii: None,
            error: Some("Format de nombre non reconnu".to_string()),
        },
    }
}

/// Calcule les caractéristiques d'un sous-réseau IPv4
pub fn calculate_subnet(ip_str: &str, cidr: u8) -> Result<SubnetResult, String> {
    if cidr > 32 {
        return Err("Le masque CIDR doit être compris entre 0 et 32".to_string());
    }

    let parts: Vec<&str> = ip_str.split('.').collect();
    if parts.len() != 4 {
        return Err("Adresse IPv4 invalide (format attendu: x.x.x.x)".to_string());
    }

    let mut ip_num: u32 = 0;
    for part in parts {
        let octet: u32 = part.parse().map_err(|_| "Octet invalide dans l'adresse IP")?;
        if octet > 255 {
            return Err("Octet hors limites (0-255)".to_string());
        }
        ip_num = (ip_num << 8) | octet;
    }

    let mask_num: u32 = if cidr == 0 {
        0
    } else {
        !0u32 << (32 - cidr)
    };

    let net_num = ip_num & mask_num;
    let bcast_num = net_num | (!mask_num);

    let format_ip = |num: u32| {
        format!(
            "{}.{}.{}.{}",
            (num >> 24) & 0xFF,
            (num >> 16) & 0xFF,
            (num >> 8) & 0xFF,
            num & 0xFF
        )
    };

    let total_hosts = if cidr >= 31 {
        if cidr == 32 { 1 } else { 2 }
    } else {
        2u64.pow((32 - cidr) as u32)
    };

    let usable_hosts = if cidr >= 31 {
        0
    } else {
        total_hosts - 2
    };

    let first_host = if cidr >= 31 {
        format_ip(net_num)
    } else {
        format_ip(net_num + 1)
    };

    let last_host = if cidr >= 31 {
        format_ip(bcast_num)
    } else {
        format_ip(bcast_num - 1)
    };

    Ok(SubnetResult {
        ip: ip_str.to_string(),
        cidr,
        netmask: format_ip(mask_num),
        network_address: format_ip(net_num),
        broadcast_address: format_ip(bcast_num),
        first_host,
        last_host,
        total_hosts,
        usable_hosts,
    })
}

/// Liste des lois d'algèbre booléenne essentielles (UNASMOH)
pub fn get_boolean_laws() -> Vec<BooleanLaw> {
    vec![
        BooleanLaw {
            name: "Loi de De Morgan 1".to_string(),
            expression: "!(A . B) = !A + !B".to_string(),
            description: "Le complément d'un produit logique est égal à la somme des compléments."
                .to_string(),
        },
        BooleanLaw {
            name: "Loi de De Morgan 2".to_string(),
            expression: "!(A + B) = !A . !B".to_string(),
            description: "Le complément d'une somme logique est égal au produit des compléments."
                .to_string(),
        },
        BooleanLaw {
            name: "Loi d'Absorption".to_string(),
            expression: "A + (A . B) = A".to_string(),
            description: "Une variable absorbe un terme qui la contient en conjonction."
                .to_string(),
        },
        BooleanLaw {
            name: "Élément Neutre ET".to_string(),
            expression: "A . 1 = A".to_string(),
            description: "1 est l'élément neutre de l'opération ET (conjonction).".to_string(),
        },
        BooleanLaw {
            name: "Élément Absorbant OU".to_string(),
            expression: "A + 1 = 1".to_string(),
            description: "1 est l'élément absorbant de l'opération OU (disjonction).".to_string(),
        },
    ]
}
