# EWB Cloud Labs: AWS VPC Peering Complete Project Kit

This repository contains the complete solution kit for the **AWS VPC Peering: Connect Two VPCs & Prove Private Connectivity** student project workbook (AWS Architect Associate).

---

## 📁 Repository Structure

```text
Aws Project/
├── Aditya_EWB_VPC_Peering.pdf      # Ready-to-submit 100-mark final evaluation PDF report
├── README.md                       # This quickstart documentation
├── MANUAL_CONSOLE_GUIDE.md         # Click-by-click AWS Management Console walkthrough
├── VIVA_AND_TECHNICAL_DEFENSE.md   # Complete answers to viva & oral defense questions
├── ssh_setup_guide.md              # Windows / Mac / Linux SSH & ProxyJump setup
│
├── cloudformation/
│   └── vpc_peering_lab.yaml        # Automated 1-Click AWS CloudFormation template
│
├── terraform/
│   ├── main.tf                     # Complete Terraform deployment code
│   ├── variables.tf                # Region, instance type & key pair variables
│   └── outputs.tf                  # Infrastructure outputs
│
└── report_generator/
    ├── report_template.html        # High-res, print-optimized HTML report template
    ├── student_data.json           # Editable student metadata & actual AWS IDs
    ├── generate_report.py          # Automatic PDF generator using headless browser
    └── compiled_report.html        # Compiled HTML report preview
```

---

## 🚀 How to Execute Your Project

You have two paths to deploy and test this architecture:

### Option 1: 1-Click Automated CloudFormation Deployment (Fastest ~ 3 mins)
If you want AWS to provision the entire architecture (VPCs, Subnets, Route Tables, Peering, SGs, and EC2s) automatically:

1. In the AWS Console, create an EC2 Key Pair named `ewb-lab` in your chosen region (e.g. `ap-south-1` Mumbai).
2. Go to **AWS CloudFormation** > **Create stack** > **With new resources (standard)**.
3. Choose **Upload a template file** and select:
   `cloudformation/vpc_peering_lab.yaml`
4. Enter Stack name: `ewb-vpc-peering-stack`.
5. Select KeyName: `ewb-lab`. Leave other defaults or enter your public IP.
6. Click **Next** through the screens and click **Submit**.
7. In ~3 minutes, the stack status will be `CREATE_COMPLETE`. Check the **Outputs** tab for your `BastionPublicIP`, `VpcAId`, `VpcBId`, and instance IDs!

---

### Option 2: Step-by-Step AWS Console Walkthrough (Click-by-Click)
If you are doing the lab manually in the AWS Management Console to capture screenshots as you go:
- Follow [MANUAL_CONSOLE_GUIDE.md](file:///c:/Users/Aditya/Downloads/Aws%20Project/MANUAL_CONSOLE_GUIDE.md).
- It covers every screen, button, CIDR, and security rule from Page 4 to Page 12 of the workbook.

---

## 🔑 SSH Setup & ProxyJump Configuration

Follow [ssh_setup_guide.md](file:///c:/Users/Aditya/Downloads/Aws%20Project/ssh_setup_guide.md) to set up your `.ssh/config`:

```ssh-config
Host ewb-bastion
    HostName <YOUR_BASTION_PUBLIC_IP>
    User ec2-user
    IdentityFile ~/.ssh/ewb-lab.pem
    IdentitiesOnly yes

Host ewb-app-a
    HostName 10.10.2.10
    User ec2-user
    IdentityFile ~/.ssh/ewb-lab.pem
    IdentitiesOnly yes
    ProxyJump ewb-bastion

Host ewb-app-b
    HostName 10.20.1.10
    User ec2-user
    IdentityFile ~/.ssh/ewb-lab.pem
    IdentitiesOnly yes
    ProxyJump ewb-bastion
```

> **Windows PowerShell Permission Fix:**
> ```powershell
> icacls.exe "$HOME\.ssh\ewb-lab.pem" /reset
> icacls.exe "$HOME\.ssh\ewb-lab.pem" /inheritance:r
> icacls.exe "$HOME\.ssh\ewb-lab.pem" /grant:r "$($env:USERNAME):(R)"
> ```

---

## 🧪 Verification & Acceptance Criteria

| # | Test | Where to Run | Command | Expected Outcome |
|---|---|---|---|---|
| **01** | **Baseline Failure** | Inside App-A (before peer routes) | `ping -c 4 10.20.1.10` | `100% packet loss` (no replies) |
| **02** | **Forward Path** | Inside App-A (after routes) | `ping -c 4 10.20.1.10` | `0% packet loss` (4 replies) |
| **03** | **Reverse Path** | Inside App-B (after routes) | `ping -c 4 10.10.2.10` | `0% packet loss` (4 replies) |
| **04** | **Private SSH** | Local terminal / PowerShell | `ssh ewb-app-b` | Shell on App-B via Bastion |
| **05** | **Isolation** | AWS EC2 Console | Inspect App-A & App-B | No public IPv4 on either host |
| **06** | **Controlled Failure** | Inside App-A | Delete ICMP rule in `ewb-sg-app-b` & ping | `100% loss`, restores on re-adding |

---

## 🎓 Viva & Defense Preparation

Before evaluation, review [VIVA_AND_TECHNICAL_DEFENSE.md](file:///c:/Users/Aditya/Downloads/Aws%20Project/VIVA_AND_TECHNICAL_DEFENSE.md) for detailed explanations of:
1. **Why is the return route needed?** (VPC routers need symmetric route entries for bidirectional reply packets).
2. **Why is the App-B SSH source the bastion private IP?** (SSH ProxyJump terminates the outer hop at Bastion; Bastion initiates the inner TCP connection using its private ENI `10.10.1.10`).
3. **Why does Active peering not guarantee a successful ping?** (Peering only establishes the link; route tables, security groups, and NACLs must each permit traffic).
4. **Can VPC B use VPC A's internet gateway over peering?** (No; AWS VPC peering is strictly non-transitive).

---

## 📄 Re-Generating Your Final PDF Report

The ready-to-submit report is pre-compiled at:
`Aditya_EWB_VPC_Peering.pdf`

If you want to update it with your real AWS IDs or specific details:
1. Open `report_generator/student_data.json` and edit your name, batch, or actual resource IDs.
2. Run:
   ```powershell
   python report_generator/generate_report.py
   ```
3. A fresh PDF will be generated instantly in the project folder.
