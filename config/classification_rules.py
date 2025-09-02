"""
Document classification rules and patterns
"""

# Document classification rules
# Each rule defines how to classify documents based on keywords and patterns
CLASSIFICATION_RULES = {
    # 財務書類
    "1001": {
        "name": "財務諸表",
        "keywords": [
            "財務諸表", "財務報告書", "financial statement",
            "貸借対照表", "損益計算書", "キャッシュフロー計算書",
            "balance sheet", "income statement"
        ],
        "priority": 150,
        "category": "financial"
    },
    
    "1002": {
        "name": "損益計算書",
        "keywords": [
            "損益計算書", "P&L", "income statement", 
            "profit and loss", "収益報告書", "営業利益"
        ],
        "priority": 140,
        "category": "financial"
    },
    
    "1003": {
        "name": "貸借対照表",
        "keywords": [
            "貸借対照表", "balance sheet", "資産負債表",
            "資産", "負債", "株主資本", "純資産"
        ],
        "priority": 140,
        "category": "financial"
    },
    
    "1004": {
        "name": "キャッシュフロー計算書",
        "keywords": [
            "キャッシュフロー計算書", "cash flow statement",
            "資金収支計算書", "現金流量計算書", "営業キャッシュフロー"
        ],
        "priority": 130,
        "category": "financial"
    },
    
    "1005": {
        "name": "予算報告書",
        "keywords": [
            "予算", "予算報告書", "budget", "年次予算",
            "予算分析", "予算書", "financial budget"
        ],
        "priority": 120,
        "category": "financial"
    },
    
    # 法的文書
    "2001": {
        "name": "契約書",
        "keywords": [
            "契約書", "合意書", "contract", "agreement",
            "利用規約", "サービス契約", "業務委託契約", "当事者合意"
        ],
        "priority": 160,
        "category": "legal"
    },
    
    "2002": {
        "name": "秘密保持契約書",
        "keywords": [
            "秘密保持契約", "NDA", "機密保持契約",
            "confidentiality", "機密情報", "秘密情報"
        ],
        "priority": 150,
        "category": "legal"
    },
    
    "2003": {
        "name": "利用規約",
        "keywords": [
            "利用規約", "使用条件", "terms of service",
            "サービス規約", "ウェブサイト規約", "user agreement"
        ],
        "priority": 130,
        "category": "legal"
    },
    
    # 報告書類
    "3001": {
        "name": "年次報告書",
        "keywords": [
            "年次報告書", "年間報告書", "annual report",
            "年度末報告書", "年次まとめ", "事業報告書"
        ],
        "priority": 140,
        "category": "reports"
    },
    
    "3002": {
        "name": "月次報告書",
        "keywords": [
            "月次報告書", "月間報告書", "monthly report",
            "月末報告書", "進捗報告書", "状況報告書"
        ],
        "priority": 130,
        "category": "reports"
    },
    
    "3003": {
        "name": "プロジェクト報告書",
        "keywords": [
            "プロジェクト報告書", "project report", "プロジェクト状況",
            "マイルストーン報告", "進捗報告", "プロジェクトサマリー"
        ],
        "priority": 120,
        "category": "reports"
    },
    
    "3004": {
        "name": "市場調査報告書",
        "keywords": [
            "市場調査", "market research", "市場分析",
            "業界レポート", "競合分析", "マーケット調査"
        ],
        "priority": 125,
        "category": "reports"
    },
    
    # 請求書類
    "4001": {
        "name": "請求書",
        "keywords": [
            "請求書", "invoice", "bill", "請求番号",
            "支払い期日", "billing", "請求金額", "お支払い"
        ],
        "priority": 170,
        "category": "billing"
    },
    
    "4002": {
        "name": "領収書",
        "keywords": [
            "領収書", "receipt", "領収証", "支払い証明",
            "入金確認書", "受領書", "支払い受領"
        ],
        "priority": 160,
        "category": "billing"
    },
    
    "4003": {
        "name": "発注書",
        "keywords": [
            "発注書", "purchase order", "注文書", "発注依頼",
            "購入依頼", "調達", "発注番号"
        ],
        "priority": 150,
        "category": "billing"
    },
    
    "4004": {
        "name": "見積書",
        "keywords": [
            "見積書", "quote", "quotation", "見積り",
            "提案書", "価格見積", "コスト見積"
        ],
        "priority": 130,
        "category": "billing"
    },
    
    # 人事書類
    "5001": {
        "name": "雇用契約書",
        "keywords": [
            "雇用契約書", "employment contract", "労働契約",
            "従業員ハンドブック", "職務記述書", "内定通知書"
        ],
        "priority": 150,
        "category": "hr"
    },
    
    "5002": {
        "name": "給与報告書",
        "keywords": [
            "給与報告書", "payroll", "給与明細", "賃金報告",
            "従業員報酬", "給与計算書", "salary report"
        ],
        "priority": 140,
        "category": "hr"
    },
    
    "5003": {
        "name": "人事評価",
        "keywords": [
            "人事評価", "performance review", "従業員評価",
            "年次評価", "査定", "人事考課", "employee assessment"
        ],
        "priority": 130,
        "category": "hr"
    },
    
    # 保険書類
    "6001": {
        "name": "保険証券",
        "keywords": [
            "保険証券", "insurance policy", "保険契約書",
            "保険番号", "保険証明書", "契約者"
        ],
        "priority": 140,
        "category": "insurance"
    },
    
    "6002": {
        "name": "保険金請求書",
        "keywords": [
            "保険金請求", "insurance claim", "請求番号",
            "事故報告書", "損害報告書", "事故証明"
        ],
        "priority": 150,
        "category": "insurance"
    },
    
    # データ・分析
    "7001": {
        "name": "データエクスポート",
        "keywords": [
            "データエクスポート", "data export", "データベース出力",
            "エクスポートデータ", "データファイル", "出力データ"
        ],
        "priority": 100,
        "category": "data"
    },
    
    "7002": {
        "name": "分析レポート",
        "keywords": [
            "分析", "analytics", "データ分析", "統計",
            "メトリクス", "ダッシュボード", "KPI", "指標"
        ],
        "priority": 110,
        "category": "data"
    },
    
    # 顧客関連書類
    "8001": {
        "name": "顧客情報",
        "keywords": [
            "顧客", "customer", "クライアント", "連絡先情報",
            "顧客データ", "顧客リスト", "取引先"
        ],
        "priority": 120,
        "category": "customer"
    },
    
    "8002": {
        "name": "顧客フィードバック",
        "keywords": [
            "顧客フィードバック", "customer feedback", "アンケート",
            "レビュー", "顧客満足度", "お客様の声", "testimonial"
        ],
        "priority": 110,
        "category": "customer"
    }
}

# カテゴリ説明
CATEGORY_DESCRIPTIONS = {
    "financial": "財務諸表、予算、会計書類",
    "legal": "契約書、合意書、法的文書",
    "reports": "事業報告書、分析、要約",
    "billing": "請求書、領収書、支払い関連書類",
    "hr": "人事・従業員関連書類",
    "insurance": "保険証券・保険金請求書",
    "data": "データエクスポート・分析レポート",
    "customer": "顧客情報・フィードバック"
}

# デフォルト分類ルール
DEFAULT_RULE = {
    "code": "9999",
    "name": "未分類文書",
    "category": "general",
    "confidence": 0.1
}