# Week 6 Assignment: Network Security Analysis & Policy Design

**Due**: End of Week 6 (see Canvas for exact deadline)  
**Points**: 25 points  
**Submission**: Submit Pull Request URL to Canvas

## 🎯 Assignment Overview

Analyze network security configurations and design security policies using industry-standard tools and practices. Your implementation should demonstrate understanding of firewall rules, network monitoring, and security policy development learned this week.

**Time Estimate**: 8-10 hours (reduced from enterprise deployment complexity)

## 📋 Requirements

### Core Functionality (70 points)

#### 1. Firewall Rule Analysis Tool (25 points)
Build a Python tool that analyzes firewall configurations:

- **Rule parser** that reads common firewall formats (iptables, pfSense XML)
- **Policy analyzer** identifying conflicts, redundancies, and gaps
- **Risk assessment** scoring rules based on security best practices
- **Report generation** with recommendations for improvement

**Example functionality**:
```python
# Your tool should analyze rules like:
firewall_analyzer = FirewallAnalyzer()
firewall_analyzer.load_rules("sample_firewall.rules")
firewall_analyzer.analyze_security_gaps()
firewall_analyzer.generate_report("security_analysis.html")
```

#### 2. Network Traffic Monitor (25 points)
Create a network monitoring tool using Python:

- **Packet capture analysis** using provided pcap files
- **Protocol analysis** identifying HTTP, HTTPS, DNS, etc.
- **Anomaly detection** finding unusual traffic patterns
- **Security event logging** identifying potential threats

**Key Features**:
- Parse common protocols and extract metadata
- Identify suspicious patterns (port scans, failed connections)
- Generate alerts for security events
- Export findings in JSON/CSV format

#### 3. Security Policy Generator (20 points)
Develop a tool that creates security policies:

- **Network segmentation planner** based on asset inventory
- **Access control matrix** defining who can access what
- **Incident response playbook** for common network threats
- **Compliance checker** against security frameworks (NIST, CIS)

### Documentation and Analysis (20 points)

Create network security analysis documentation:

```
firewall_analysis_report.md    # Analysis of provided firewall rules
network_monitoring_findings.md # Results from traffic analysis
security_policy_recommendations.md # Policy recommendations
implementation_guide.md        # How to use your tools
```

### Professional Features (10 points - Optional)

Choose one advanced feature:
- **Web dashboard** displaying security metrics
- **API integration** with threat intelligence feeds
- **Machine learning** anomaly detection
- **Automated remediation** suggestions

## 🧪 Testing and Validation

Your tools will be tested with:
- **Sample firewall configurations** (provided in resources/)
- **Network traffic captures** (pcap files provided)
- **Synthetic attack scenarios** for anomaly detection
- **Real-world policy frameworks** for compliance checking

## 📊 Grading Rubric

### Technical Implementation (70 points)
- **Firewall Analysis (25 pts)**: Rule parsing, conflict detection, recommendations
- **Traffic Monitoring (25 pts)**: Packet analysis, anomaly detection, alerting  
- **Policy Generation (20 pts)**: Segmentation planning, access controls, compliance

### Documentation Quality (20 points)
- **Clear analysis reports** with actionable recommendations
- **Professional documentation** suitable for security teams
- **Implementation guides** enabling tool usage

### Code Quality (10 points)
- **Clean, readable code** with appropriate comments
- **Error handling** for malformed inputs
- **Modular design** enabling code reuse

## 🔍 Self-Assessment Questions

Before submitting, ask yourself:

1. **Can my tools actually help a security analyst?**
2. **Do my analyses provide actionable insights?**
3. **Would I trust my recommendations in a real environment?**
4. **Is my code robust enough for production use?**
5. **Do my reports communicate clearly to both technical and management audiences?**

## 📤 Submission Instructions

### Step 1: Create Pull Request
1. **Push your code** to your forked repository:
   ```bash
   git add .
   git commit -m "Complete Week 6 network security analysis tools"
   git push origin week06-assignment
   ```

2. **Create Pull Request** on GitHub with description including:
   - Summary of tools developed
   - Key analysis findings from sample data
   - Challenges encountered and solutions
   - Testing approach used

### Step 2: Submit to Canvas
1. **Copy the Pull Request URL**
2. **Go to Canvas** → Week 6 Assignment  
3. **Paste the PR URL** in the submission box
4. **Submit**

### Required Files in Your PR
- `firewall_analyzer.py` - Firewall rule analysis tool
- `traffic_monitor.py` - Network traffic analysis tool
- `policy_generator.py` - Security policy creation tool
- `requirements.txt` - Python dependencies
- `README.md` - Tool usage and setup instructions
- `analysis_reports/` - Your analysis of provided sample data
- `test_data/` - Sample inputs for testing (if created)

**Resources Provided**:
- Sample firewall configurations in multiple formats
- Network traffic captures (pcap files)
- Security policy templates and frameworks
- Analysis report examples

---

**Need Help?**
- Check [troubleshooting guide](../resources/troubleshooting.md)
- Post questions in Canvas discussions  
- Attend office hours for architecture guidance