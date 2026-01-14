from mextmock.utils import get_ordering_parameter

order = {

    "id": "ORD-3937-2670-9304",
    "revision": 4,
    "type": "Purchase",
    "status": "Processing",
    "notes": "",
    "template": {
        "id": "TPL-8373-4303-0001",
        "name": "Sample order processing template",
        "revision": 1
    },
    "listing": {
        "id": "LST-7173-0654",
        "name": "LST-7173-0654",
        "revision": 1,
        "priceList": {
            "id": "PRC-8373-4303-0001",
            "revision": 1,
            "currency": "USD",
            "precision": 2,
            "externalIds": {},
            "statistics": {
                "sellers": 1,
                "listings": 1,
                "priceListItems": 2,
                "purchasePriceItems": 2,
                "purchasePriceCompleteness": 100
            },
            "product": {
                "id": "PRD-8373-4303",
                "name": "Arancino",
                "icon": "/v1/catalog/products/PRD-8373-4303/icon",
                "revision": 4,
                "externalIds": {},
                "status": "Published"
            },
            "vendor": {
                "id": "ACC-1671-9270",
                "name": "Antonio & Ciccio Delizie di Sicilia S.p.A.",
                "icon": "/v1/accounts/accounts/ACC-1671-9270/icon",
                "revision": 6,
                "type": "Vendor",
                "status": "Active"
            },
            "audit": {
                "created": {
                    "at": "2025-11-26T11:21:33.502Z",
                    "by": {
                        "id": "USR-8813-4917",
                        "name": "Antonio Di Mariano",
                        "revision": 1
                    }
                }
            }
        }
    },
    "authorization": {
        "id": "AUT-0022-6779",
        "name": "Antonio",
        "revision": 1,
        "currency": "USD"
    },
    "agreement": {
        "id": "AGR-6306-8883-8280",
        "name": "Arancino for Pippo Pappo",
        "revision": 3,
        "status": "Provisioning",
        "listing": {
            "id": "LST-7173-0654",
            "name": "LST-7173-0654",
            "revision": 1
        },
        "authorization": {
            "id": "AUT-0022-6779",
            "name": "Antonio",
            "revision": 1,
            "currency": "USD"
        },
        "vendor": {
            "id": "ACC-1671-9270",
            "name": "Antonio & Ciccio Delizie di Sicilia S.p.A.",
            "icon": "/v1/accounts/accounts/ACC-1671-9270/icon",
            "revision": 6,
            "type": "Vendor",
            "status": "Active"
        },
        "client": {
            "id": "ACC-2200-4891",
            "name": "Pippo Pappo",
            "revision": 2,
            "type": "Client",
            "status": "Enabled"
        },
        "price": {
            "PPxY": 0,
            "PPxM": 0,
            "currency": "USD"
        },
        "template": {
            "id": "TPL-8373-4303-0001",
            "name": "Sample order processing template",
            "revision": 1
        },
        "assets": [],
        "subscriptions": [],
        "licensee": {
            "id": "LCE-2789-4339-7035",
            "name": "Geronimo",
            "revision": 1
        },
        "buyer": {
            "id": "BUY-4356-3691",
            "name": "MiPiaciTu",
            "revision": 1
        },
        "seller": {
            "id": "SEL-7032-1456",
            "name": "SoftwareONE Inc.",
            "revision": 1,
            "externalId": "US"
        },
        "product": {
            "id": "PRD-8373-4303",
            "name": "Arancino",
            "icon": "/v1/catalog/products/PRD-8373-4303/icon",
            "revision": 4,
            "externalIds": {},
            "status": "Published"
        },
        "externalIds": {
            "client": ""
        },
        "termsAndConditions": [],
        "certificates": [],
        "audit": {
            "created": {
                "at": "2025-12-01T14:40:00.091Z",
                "by": {
                    "id": "USR-3132-5980",
                    "name": "Francesco Faraone",
                    "revision": 1
                }
            },
            "updated": {
                "at": "2025-12-01T14:48:58.370Z",
                "by": {
                    "id": "USR-3132-5980",
                    "name": "Francesco Faraone",
                    "revision": 1
                }
            }
        }
    },
    "assignee": {
        "id": "USR-3132-5980",
        "name": "Francesco Faraone",
        "icon": "/v1/accounts/users/USR-3132-5980/icon",
        "revision": 1
    },
    "externalIds": {
        "client": ""
    },
    "price": {
        "PPx1": 0,
        "PPxY": 960,
        "PPxM": 80,
        "currency": "USD"
    },
    "lines": [
        {
            "id": "ALI-6306-8883-8280-0001",
            "oldQuantity": 0,
            "quantity": 1,
            "price": {
                "PPxY": 960,
                "PPxM": 80,
                "unitPP": 80,
                "currency": "USD"
            },
            "item": {
                "id": "ITM-8373-4303-0002",
                "name": "Ripieno alla norma",
                "revision": 3,
                "description": "muy bueno",
                "externalIds": {
                    "vendor": "ARANCINO-456-456"
                },
                "group": {
                    "id": "IGR-8373-4303-0001",
                    "name": "Items",
                    "revision": 3
                },
                "unit": {
                    "id": "UNT-5894",
                    "name": "Benefit",
                    "revision": 1,
                    "description": "Benefits are advantages or privileges associated with certain subscriptions or programs. These can include access to premium features, priority support, training resources, or discounts on additional services."
                },
                "terms": {
                    "model": "quantity",
                    "period": "1m",
                    "commitment": "1m"
                },
                "quantityNotApplicable": False,
                "status": "Published",
                "product": {
                    "id": "PRD-8373-4303",
                    "name": "Arancino",
                    "icon": "/v1/catalog/products/PRD-8373-4303/icon",
                    "revision": 4,
                    "externalIds": {},
                    "status": "Published"
                },
                "parameters": [],
                "audit": {
                    "pending": {
                        "at": "2025-11-26T11:26:46.309Z",
                        "by": {
                            "id": "USR-8813-4917",
                            "name": "Antonio Di Mariano",
                            "revision": 1
                        }
                    },
                    "published": {
                        "at": "2025-11-26T11:30:22.236Z",
                        "by": {
                            "id": "USR-8813-4917",
                            "name": "Antonio Di Mariano",
                            "revision": 1
                        }
                    },
                    "created": {
                        "at": "2025-11-26T11:13:43.906Z",
                        "by": {
                            "id": "USR-8813-4917",
                            "name": "Antonio Di Mariano",
                            "revision": 1
                        }
                    },
                    "updated": {
                        "at": "2025-11-26T11:30:22.236Z",
                        "by": {
                            "id": "USR-8813-4917",
                            "name": "Antonio Di Mariano",
                            "revision": 1
                        }
                    }
                }
            },
            "agreement": {
                "id": "AGR-6306-8883-8280",
                "name": "Arancino for Pippo Pappo",
                "revision": 3,
                "status": "Provisioning"
            },
            "order": {
                "id": "ORD-3937-2670-9304",
                "revision": 4
            },
            "client": {
                "id": "ACC-2200-4891",
                "name": "Pippo Pappo",
                "revision": 2,
                "type": "Client",
                "status": "Enabled"
            },
            "vendor": {
                "id": "ACC-1671-9270",
                "name": "Antonio & Ciccio Delizie di Sicilia S.p.A.",
                "icon": "/v1/accounts/accounts/ACC-1671-9270/icon",
                "revision": 6,
                "type": "Vendor",
                "status": "Active"
            },
            "buyer": {
                "id": "BUY-4356-3691",
                "name": "MiPiaciTu",
                "revision": 1
            },
            "seller": {
                "id": "SEL-7032-1456",
                "name": "SoftwareONE Inc.",
                "revision": 1,
                "externalId": "US"
            },
            "product": {
                "id": "PRD-8373-4303",
                "name": "Arancino",
                "icon": "/v1/catalog/products/PRD-8373-4303/icon",
                "revision": 4,
                "externalIds": {},
                "status": "Published"
            }
        }
    ],
    "subscriptions": [],
    "assets": [],
    "parameters": {
        "ordering": [
            {
                "id": "PAR-8373-4303-0001",
                "externalId": "scenario",
                "name": "scenario",
                "type": "DropDown",
                "phase": "Order",
                "displayValue": "simple",
                "value": "simple"
            }
        ],
        "fulfillment": [
            {
                "id": "PAR-8373-4303-0002",
                "externalId": "task_id",
                "name": "taskID",
                "type": "SingleLineText",
                "phase": "Fulfillment",
                "displayValue": "TSK-1234-5678-9012",
                "value": "TSK-1234-5678-9012"
            }
        ]
    },
    "product": {
        "id": "PRD-8373-4303",
        "name": "Arancino",
        "icon": "/v1/catalog/products/PRD-8373-4303/icon",
        "revision": 4,
        "externalIds": {},
        "status": "Published"
    },
    "client": {
        "id": "ACC-2200-4891",
        "name": "Pippo Pappo",
        "revision": 2,
        "type": "Client",
        "status": "Enabled"
    },
    "licensee": {
        "id": "LCE-2789-4339-7035",
        "name": "Geronimo",
        "revision": 1,
        "eligibility": {
            "client": True,
            "partner": False
        }
    },
    "buyer": {
        "id": "BUY-4356-3691",
        "name": "MiPiaciTu",
        "revision": 1
    },
    "seller": {
        "id": "SEL-7032-1456",
        "name": "SoftwareONE Inc.",
        "revision": 1,
        "externalId": "US"
    },
    "vendor": {
        "id": "ACC-1671-9270",
        "name": "Antonio & Ciccio Delizie di Sicilia S.p.A.",
        "icon": "/v1/accounts/accounts/ACC-1671-9270/icon",
        "revision": 6,
        "type": "Vendor",
        "status": "Active"
    },
    "termsAndConditions": [],
    "certificates": [],
    "audit": {
        "processing": {
            "at": "2025-12-01T14:48:58.369Z",
            "by": {
                "id": "USR-3132-5980",
                "name": "Francesco Faraone",
                "revision": 1
            }
        },
        "created": {
            "at": "2025-12-01T14:40:01.895Z",
            "by": {
                "id": "USR-3132-5980",
                "name": "Francesco Faraone",
                "revision": 1
            }
        },
        "updated": {
            "at": "2025-12-02T11:09:35.600Z",
            "by": {
                "id": "USR-3132-5980",
                "name": "Francesco Faraone",
                "revision": 1
            }
        }
    }
}

def test_order():
    t = get_ordering_parameter(order,"scenario")
    assert t is not None