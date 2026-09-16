"""20+ Specialized Problem-Mining & Search Algorithms.
Each algorithm targets a specific vector of real-world friction, economic leakage,
and unsexy operational bottlenecks across B2B, industrial, logistics, and trade domains.
"""

from typing import Dict, List
from oppscout.models import PainPointSignal, UserProfile


class SpecializedSearchAlgorithms:
    """Library of 20+ distinct algorithmic vectors designed to uncover
    non-obvious, high-urgency market problems.
    """

    ALGORITHMS_REGISTRY: Dict[str, Dict] = {
        # 1. Spreadsheet Hell & Manual Workflow Friction
        "SpreadsheetHellAlgorithm": {
            "name": "Spreadsheet Hell & Manual Data Re-entry",
            "query_template": '"{domain}" manual spreadsheet nightmare OR "still using excel" OR "copy paste"',
            "focus": "Operators wasting 3-5 hours daily typing numbers from paper/WhatsApp into Excel.",
            "urgency": "High",
            "typical_leakage": "₹15,000 - ₹35,000/month in wasted clerical payroll + clerical error rate."
        },

        # 2. Delayed B2B Invoicing & Discrepancy Reconciliation
        "InvoiceLeakageAlgorithm": {
            "name": "Invoice Reconciliation & Billing Discrepancy",
            "query_template": '"{domain}" invoice dispute OR "unreconciled" OR "delayed payment" OR "discrepancy"',
            "focus": "Mismatched line items between purchase orders, delivery notes, and tax invoices holding up 20% payments.",
            "urgency": "Critical",
            "typical_leakage": "10-18% of monthly working capital locked in disputed receivables."
        },

        # 3. Regulatory Penalties, Inspections & Seizures
        "RegulatoryPenaltyAlgorithm": {
            "name": "Regulatory Penalties & Highway Checkpost Seizures",
            "query_template": '"{location}" "{domain}" penalty fine seizure compliance inspector OR "rule 138"',
            "focus": "24-hour E-Waybill expiration, GST mismatches, pollution board or factory inspectorate compounding fines.",
            "urgency": "Extreme",
            "typical_leakage": "₹50,000 to ₹2,00,000 per compounding vehicle detention or plant notice."
        },

        # 4. Physical Theft & Transit Shrinkage
        "PhysicalTheftPilferageAlgorithm": {
            "name": "Diesel Siphoning & Transit Shrinkage",
            "query_template": '"{domain}" diesel theft OR "fuel pilferage" OR "shrinkage" OR "cargo lost"',
            "focus": "Drivers siphoning diesel at unmonitored highway stops or warehouse staff skimming raw materials.",
            "urgency": "High",
            "typical_leakage": "₹12,000 - ₹25,000 per heavy vehicle monthly in stolen fuel."
        },

        # 5. Quality Disputes & Batch Variation Rejections
        "BatchRejectionAlgorithm": {
            "name": "Batch Variation & Quality Rejection at Delivery",
            "query_template": '"{domain}" batch mismatch OR "quality rejection" OR "color defect" OR "finish problem"',
            "focus": "In marble, ceramics, and textiles: master operators eyeball mixing, leading to client delivery rejections.",
            "urgency": "Critical",
            "typical_leakage": "₹1,50,000 - ₹5,00,000 in rejected outward lots and delayed project sign-offs."
        },

        # 6. Unscheduled Emergency Machinery Downtime
        "EmergencyBreakdownAlgorithm": {
            "name": "Unscheduled Motor & Spindle Burnouts",
            "query_template": '"{domain}" breakdown machine downtime motor burnout "repair delayed"',
            "focus": "Small plants skipping thermal/vibration diagnostics until main spindle or loom burns out.",
            "urgency": "High",
            "typical_leakage": "₹20,000 - ₹50,000 per hour of halted plant production."
        },

        # 7. Cold-Chain Temperature Integrity Loss
        "ColdChainLossAlgorithm": {
            "name": "Cold-Chain Temperature Abuse in Transit",
            "query_template": '"{domain}" cold chain spoilage temperature fluctuation perishable rot',
            "focus": "Reefer drivers turning off cooling compressors at night halts to pocket diesel money.",
            "urgency": "High",
            "typical_leakage": "30-50% distress price discounts on heat-damaged produce/pharma consignments."
        },

        # 8. Expired Stock & Dead Working Capital
        "DeadInventoryAlgorithm": {
            "name": "Expired Inventory & Distributor Credit Deadlock",
            "query_template": '"{domain}" expired stock inventory write-off return distributor credit note',
            "focus": "Independent pharmacies and retailers losing margins on expired unsold boxes waiting months for credit notes.",
            "urgency": "Medium-High",
            "typical_leakage": "4-8% net annual profit wiped out in inventory write-offs."
        },

        # 9. Informal Ledger (Khata) & Uncollectible Credit
        "InformalCreditRecoveryAlgorithm": {
            "name": "Informal B2B Credit Default & Disputed Ledgers",
            "query_template": '"{domain}" khata credit recovery default dispute "uncollectible receivables"',
            "focus": "Wholesale distributors extending 30-day credit on paper cards; retailers dispute deliveries 45 days later.",
            "urgency": "Critical",
            "typical_leakage": "3-6% bad debt write-offs on annual gross turnover."
        },

        # 10. Single-Point-of-Failure Knowledge Bottleneck
        "StaffKnowledgeLeakAlgorithm": {
            "name": "Master Artisan / Technician Single-Point Failure",
            "query_template": '"{domain}" operator absent production stopped skilled technician bottleneck',
            "focus": "Factory operations halting completely when the 1 master dye mixer or CNC programmer takes sick leave.",
            "urgency": "High",
            "typical_leakage": "Complete operational paralysis and missed customer delivery deadlines."
        },

        # 11. Opaque Concierge Sub-Contracting Brokerages
        "BrokerageOpacityAlgorithm": {
            "name": "Fragmented Subcontractor Brokerages with 15% Markups",
            "query_template": '"{domain}" middleman cut broker commission subcontractor transparency delay',
            "focus": "Businesses needing urgent specialized job work relying on telephone brokers who charge huge markups.",
            "urgency": "Medium",
            "typical_leakage": "12-15% margin siphoned by non-value-adding phone brokers."
        },

        # 12. Proof-of-Delivery Lost Carbon Copies
        "ProofOfDeliveryLossAlgorithm": {
            "name": "Lost Physical Carbon Copies & Delivery Dispute",
            "query_template": '"{domain}" delivery challan lost signed receipt proof of delivery dispute',
            "focus": "Signed paper delivery slips getting crumpled or lost in delivery vans, blocking payments for 60 days.",
            "urgency": "High",
            "typical_leakage": "Cashflow freeze on 100% of the invoice until delivery is re-verified."
        },

        # 13. Pre-Audit Inspection Panic
        "ComplianceAuditPanicAlgorithm": {
            "name": "Pre-Audit Document Scramble & Fine Avoidance",
            "query_template": '"{domain}" audit panic compliance records safety inspection last minute',
            "focus": "SMEs scrambling for 3 days before ISO/Pollution/Tax audits to fabricate missing inspection logs.",
            "urgency": "Medium-High",
            "typical_leakage": "Hundreds of management hours lost + vulnerability to penalty notices."
        },

        # 14. Asset Underutilization & Empty Return Runs
        "EmptyMilesAlgorithm": {
            "name": "Empty Return-Trip Running & Idle Equipment",
            "query_template": '"{domain}" empty miles return trip underutilized idle capacity',
            "focus": "Freight trucks returning empty after delivering outbound cargo; 35% of trip cost wasted on air.",
            "urgency": "High",
            "typical_leakage": "30-35% margin compression on round-trip haulage."
        },

        # 15. Port Demurrage & Customs Clearance Bottlenecks
        "CustomsDemurrageAlgorithm": {
            "name": "Port Demurrage Charges & Documentation Stalls",
            "query_template": '"{domain}" port demurrage detention customs clearance delay container fine',
            "focus": "Exporters paying ₹8,000-₹20,000/day per container in port storage penalties due to 1 missing certification.",
            "urgency": "Critical",
            "typical_leakage": "Thousands of dollars in compounding demurrage fees at container freight stations."
        },

        # 16. WhatsApp Group Workflow Chaos
        "WhatsAppChaosAlgorithm": {
            "name": "Critical Approvals & Orders Buried in WhatsApp Groups",
            "query_template": '"{domain}" whatsapp order lost missing photo chat approval mistake',
            "focus": "Managers tracking 200 daily purchase requests across 15 noisy WhatsApp groups, dropping 5-10% of orders.",
            "urgency": "Medium-High",
            "typical_leakage": "Customer churn and delayed fulfillment due to missed message threads."
        },

        # 17. Raw Material Batch Price Volatility
        "MaterialPriceVolatilityAlgorithm": {
            "name": "Raw Material Price Spike Squeezing Fixed Contracts",
            "query_template": '"{domain}" raw material price hike margin squeeze scrap cost increase',
            "focus": "Manufacturers bound by fixed-price client quotes while input commodity prices surge 20% in 1 week.",
            "urgency": "High",
            "typical_leakage": "Entire net profit wiped out on delivered orders."
        },

        # 18. Diagnostic Sample Specimen Invalidation
        "SpecimenDegradationAlgorithm": {
            "name": "Tier-2 Diagnostic Blood Sample Hemolysis in Transit",
            "query_template": '"{domain}" sample hemolysis specimen transit delay courier invalid',
            "focus": "Blood samples collected on motorbikes in Tier-2/3 towns spoiling in 42°C heat before reaching central lab.",
            "urgency": "High",
            "typical_leakage": "Reputational disaster and cost of re-collecting samples from angry patients."
        },

        # 19. Diesel Generator (DG) & Power Load-Shedding Overheads
        "PowerOverheadAlgorithm": {
            "name": "Captive Diesel Generator Power Overheads in Industrial Belts",
            "query_template": '"{domain}" diesel generator power cut industrial power tariff cost load shedding',
            "focus": "Industrial units running expensive DG power at ₹28/unit compared to ₹9/unit grid power during scheduled cuts.",
            "urgency": "Medium",
            "typical_leakage": "₹80,000 - ₹2,00,000 monthly diesel bill for emergency plant power."
        },

        # 20. Subcontractor Work Defect Mismatch
        "SubcontractorDefectAlgorithm": {
            "name": "Outsourced Job Work Plating & Casting Defect Rate",
            "query_template": '"{domain}" subcontractor defect job work rejected tolerance mismatch',
            "focus": "Outsourced electroplating, casting, or stitching returning with 15% tolerance defect, delaying final assembly.",
            "urgency": "Critical",
            "typical_leakage": "Scrapped parts and broken delivery SLAs with Tier-1 buyers."
        },

        # 21. The $100k Enterprise Software Void (Micro-SaaS Underserved Gap)
        "EnterpriseSoftwareVoidAlgorithm": {
            "name": "The Enterprise Software Gap (SAP/Oracle Too Expensive)",
            "query_template": '"{domain}" software too expensive small business "cannot afford SAP" alternative',
            "focus": "Mid-sized businesses needing basic automation but priced out by enterprise ERPs charging ₹25L+ upfront.",
            "urgency": "High",
            "typical_leakage": "Forced into messy manual workarounds because no right-sized $100/mo tool exists."
        }
    }

    @classmethod
    def get_all_algorithm_names(cls) -> List[str]:
        return list(cls.ALGORITHMS_REGISTRY.keys())

    @classmethod
    def get_queries_for_profile(
        cls,
        domain: str,
        location: str = "Regional Market",
        selected_algorithms: List[str] = None
    ) -> List[Dict]:
        """Generates targeted query vectors using the specialized algorithms."""
        results = []
        algo_keys = selected_algorithms or cls.ALGORITHMS_REGISTRY.keys()

        for key in algo_keys:
            algo = cls.ALGORITHMS_REGISTRY.get(key)
            if not algo:
                continue
            query = algo["query_template"].replace("{domain}", domain).replace("{location}", location)
            results.append({
                "algorithm_id": key,
                "name": algo["name"],
                "query": query,
                "focus": algo["focus"],
                "urgency": algo["urgency"],
                "leakage": algo["typical_leakage"]
            })
        return results
