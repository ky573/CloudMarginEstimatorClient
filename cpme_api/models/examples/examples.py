

products_200 = {
    "business_date": 20180809,
    "live": 'false',
    "live_timestamp": 0,
    "products": [
        {
            "clearing_house": "EUXCDEFF",
            "currency": "CHF",
            "exercise_style_flag": "E",
            "extended_product_type": 'null',
            "final_settlement_time": "09:00",
            "instrument_type": "option",
            "liquidation_group": "PEQ01",
            "margin_style_flag": "T",
            "prod_isin": "CH0008616382",
            "prod_name": "OPT ON SWISS MARKET INDEX",
            "product": "OSMI",
            "product_settlement_type": "CASH",
            "product_tick_size": 0.1,
            "product_tick_value": 1,
            "product_type": "OINX",
            "underlying_isin": "CH0009980894",
            "xm_eligibility": 'false'
        }
    ]
}

series_200 = {
    "business_date": 20180809,
    "list_series": [
        {
            "call_put_flag": "C",
            "contract_date": 20190621,
            "contract_maturity": 201906,
            "exercise_price": 160,
            "expiry_maturity": 201906,
            "iid": 18249016,
            "product_id": "OGBL",
            "version_number": "0"
        }
    ],
    "live": 'false',
    "live_timestamp": 0
}

securities_200 = {
    "business_date": 20180809,
    "live": 'false',
    "live_timestamp": 0,
    "securities": [
        {
            "basket_isin": 'false',
            "currency": "EUR",
            "iid": 1769,
            "margin_class_code": "DB10",
            "price_unit": "ABSOLUTE",
            "sec_id": "DB1",
            "sec_isin": "DE0005810055",
            "sec_name": "DEUTSCHE BOERSE AG",
            "sec_type": "SAKT",
            "security_mnemonic": "DB1",
            "security_subtype": "EQUITY",
            "standard_settlement_period": 2
        },
        {
            "basket_isin": 'false',
            "currency": "CHF",
            "iid": 13528248,
            "margin_class_code": "S0055",
            "price_unit": "PERCENTAGE",
            "sec_id": 'null',
            "sec_isin": "CH0224397171",
            "sec_name": "EIDGENOSSENSCHAFT 15-30",
            "sec_type": "BCNF",
            "security_mnemonic": 'null',
            "security_subtype": "BOND",
            "standard_settlement_period": 3
        }
    ]
}

clearing_currencies_200 = {
    "business_date": 20180809,
    "clearing_currencies": [
        "EUR",
        "CHF",
        "USD",
        "GBP"
    ],
    "live": 'false',
    "live_timestamp": 0
}

snapshots_200 = {
    "snapshots": [
        {
            "business_date": 20180809,
            "cash_available": 'false',
            "live": 'false',
            "otc_available": 'true'
        },
        {
            "business_date": 20180810,
            "cash_available": 'false',
            "live": 'true',
            "otc_available": 'true'
        }
    ]
}

live_snapshots_200 = {
    "snapshots": [
        {
            "business_date": 20180809,
            "cash_available": 'false',
            "live": 'true',
            "live_timestamp": 0,
            "otc_available": 'true'
        },
        {
            "business_date": 20180809,
            "cash_available": 'false',
            "live": 'true',
            "live_timestamp": 1562162876,
            "otc_available": 'true'
        }
    ]
}

estimator = {
    "portfolio_components": [
        {
            "etd_portfolio": [
                {
                    "contract_date": 20301220,
                    "line_no": 1,
                    "net_ls_balance": 10,
                    "product_id": "FEXD"
                },
                {
                    "call_put_flag": "C",
                    "contract_date": 20311222,
                    "exercise_price": 90,
                    "line_no": 2,
                    "net_ls_balance": -10,
                    "product_id": "OESD"
                }
            ],
            "type": "etd_portfolio"
        }
    ]
}

estimator_200 = {
    "business_date": 20180809,
    "clearing_currency": "EUR",
    "drilldowns": [
        {
            "call_put_flag": "C",
            "component_margin": 2382.083819,
            "component_margin_currency": "EUR",
            "contract_date": 20311222,
            "exercise_price": 90,
            "iid": 18249016,
            "line_no": 1,
            "liquidation_group": "PFI01",
            "liquidation_group_split": "PFI01_HP2_T0-99999",
            "maturity": 203112,
            "net_ls_balance": 10,
            "premium_margin": 0,
            "premium_margin_currency": "EUR",
            "product_id": "OEXD",
            "version_number": "0"
        }
    ],
    "errors": [
        {
            "error_msg": "Line 1 instrument iid not recognized: 736947",
            "line_no": 2,
            "portfolio": "ETD"
        }
    ],
    "live": 'false',
    "live_timestamp": 0,
    "portfolio_margin": [
        {
            "initial_margin": 3161.708587,
            "liquidation_group": "PEQ01",
            "liquidation_group_split": "PFI01_HP2_T0-99999",
            "liquidity_addon": 6.442439,
            "long_option_credit": 0,
            "market_risk": 3155.266149,
            "market_risk_per_rms": [
                {
                    "rms_components": [
                        {
                            "compression_adjustment": 10,
                            "correlation_break_adjustment": 500,
                            "risk_measure_value": 4481.692879,
                            "subsample_id": 1
                        }
                    ],
                    "rms_market_risk": 4991.692879,
                    "rms_name": "FILTERED_HISTORICAL_VAR_2",
                    "simulation_type": "Historical",
                    "weighting_factor": 0.51
                }
            ],
            "premium_margin": 0,
            "time_to_expiry_adjustment": 0
        }
    ],
    "rbm_margin": {
        "margin_classes": [
            {
                "additional_margin": 1026812,
                "additional_margin_before_grouping": 1026812,
                "cash_interest_rate": -0.566,
                "current_liquidating_margin": 851977,
                "margin_class_code": "DB10",
                "margin_class_currency": "EUR",
                "margin_group_code": 'null',
                "margin_parameter": 5.5,
                "margin_parameter_flag": "P",
                "positions": [
                    {
                        "amount_clv_cash": -10310484,
                        "amount_clv_secu": 62100,
                        "current_liquidating_margin": 851977,
                        "line_no": 1,
                        "net_cash_position": -10310484,
                        "net_security_position": 64100,
                        "sec_isin": "DE0005810055",
                        "sec_name": "DEUTSCHE BOERSE AG",
                        "settlement_date": 20210312
                    }
                ]
            },
            {
                "additional_margin": 6,
                "additional_margin_before_grouping": 6,
                "cash_interest_rate": 0.02,
                "current_liquidating_margin": -9592,
                "margin_class_code": "C004I",
                "margin_class_currency": "USD",
                "margin_group_code": 'null',
                "margin_parameter": 2.35,
                "margin_parameter_flag": "P",
                "positions": [
                    {
                        "amount_clv_cash": 10661,
                        "amount_clv_secu": 10680,
                        "current_liquidating_margin": -9592,
                        "line_no": 2,
                        "net_cash_position": 10661,
                        "net_security_position": -1066,
                        "sec_isin": "US240718A929",
                        "sec_name": 'null',
                        "settlement_date": 20210312
                    }
                ]
            }
        ]
    }
}

otc_trade_details = {
    "portfolio_components": [
        {
            "otc_csv": {
                "csv": "internalTradeID,tradeType,currency,effectiveDate,terminationDate,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod\\n1,FRA,EUR,20/12/2018,20/08/2019,fixedLeg,0.15,,,100000000,3M,,,,,,,,ACT/360,,,,,floatingLeg,,,,100000000,3M,,,,,,,,ACT/360,,,,"
            },
            "type": "otc_csv"
        }
    ]
}

otc_trade_details_200 = {
    "business_date": 20180809,
    "live": 'false',
    "live_timestamp": 0,
    "otc_trade_details": [
        {
            "maturity": "0.8Y",
            "notional": 100000000,
            "notional_currency": "EUR",
            "pay": "Fixed 0.15%",
            "receive": "EUR-EURIBOR-3M",
            "trade_id": "1",
            "type": "FRA"
        }
    ]
}

otc_sensitivities = {
    "portfolio_components": [
        {
            "otc_csv": {
                "csv": "internalTradeID,tradeType,currency,effectiveDate,terminationDate,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod\\n1,FRA,EUR,20/12/2018,20/08/2019,fixedLeg,0.15,,,100000000,3M,,,,,,,,ACT/360,,,,,floatingLeg,,,,100000000,3M,,,,,,,,ACT/360,,,,"
            },
            "type": "otc_csv"
        }
    ]
}

otc_sensitivities_200 = {
    "business_date": 20180809,
    "csv": "Maturity,EUR.ESTR\\nON,123.456",
    "curves": [
        "EUR.ESTR"
    ],
    "dv01_per_maturity": [
        {
            "dv01": [
                123.456
            ],
            "maturity": "ON"
        }
    ],
    "live": 'false',
    "live_timestamp": 0
}

greeks = {
    "greek_types": [
        "EURO_DELTA",
        "EURO_VEGA"
    ],
    "iids": [
        26807581,
        27471356
    ],
    "underlying_shifts_rel": [
        -0.01,
        0.01
    ]
}

greeks_200 = {
    "business_date": 20180809,
    "greek_types": [
        "EURO_DELTA"
    ],
    "greeks": [
        {
            "iid": 26807581,
            "values": [
                [
                    674,
                    565
                ]
            ]
        },
        {
            "iid": 27471356,
            "values": [
                [
                    0.65957,
                    0.6809
                ]
            ]
        }
    ],
    "live": 'false',
    "live_timestamp": 0,
    "underlying_shifts_rel": [
        -0.01,
        0.01
    ]
}

stressmatrix = {
    "iids": [
        26807581,
        27471356
    ],
    "underlying_shifts_rel": [
        0.01
    ],
    "volatility_shift_type": "ABSOLUTE",
    "volatility_shifts": [
        -0.1,
        0.1
    ]
}

stressmatrix_200 = {
    "business_date": 20180809,
    "live": 'false',
    "live_timestamp": 0,
    "stress_matrix": [
        {
            "iid": 26807581,
            "values": [
                [
                    0.65957
                ],
                [
                    0.6809
                ]
            ]
        },
        {
            "iid": 27471356,
            "values": [
                [
                    0.65957
                ],
                [
                    0.6809
                ]
            ]
        }
    ],
    "underlying_shifts_rel": [
        0.01
    ],
    "volatility_shift_type": "RELATIVE",
    "volatility_shifts": [
        -0.1,
        0.1
    ]
}

indicative_margin_200 = {
    "business_date": 20210622,
    "list_margins": [
        {
            "liquidation_group": "PEQ01",
            "long_initial_margin": 0.100004254,
            "long_initial_margin_cash": 1479.062914,
            "margin_currency": "EUR",
            "prod_name": "FUT ON DT. BOERSE AG",
            "product_id": "DB1H",
            "short_initial_margin": 0.11544631,
            "short_initial_margin_cash": 1707.450925
        }
    ],
    "live": 'false',
    "live_timestamp": 0
}

config_200 = {
    "max_body_size": 262144000
}

default_fund = {
    "portfolio_components": [
        {
            "etd_portfolio": [
                {
                    "contract_date": 20301220,
                    "line_no": 1,
                    "net_ls_balance": 10,
                    "product_id": "FEXD"
                },
                {
                    "call_put_flag": "C",
                    "contract_date": 20311222,
                    "exercise_price": 90,
                    "line_no": 2,
                    "net_ls_balance": -10,
                    "product_id": "OEXD"
                }
            ],
            "type": "etd_portfolio"
        }
    ]
}

default_fund_200 = {
    "business_date": 20220905,
    "clearing_currency": "EUR",
    "default_fund_contribution": {
        "currency": "EUR",
        "default_fund_requirement": 16634756,
        "slom_drilldown": [
            {
                "global_scenario": "Lehman crash 15.09.2008",
                "slom_per_lg_mg": [
                    {
                        "liquidation_group": "PEQ01",
                        "margin_group_code": 'null',
                        "slom_per_lgs_mc": [
                            {
                                "liquidation_group_split": "PEQ01_HP3",
                                "margin_class_code": 'null',
                                "stress_loss_over_margin": 167471.0,
                                "stress_value_liquidity_risk": -121.0,
                                "stress_value_market_risk": 53.0,
                                "total_margin_requirement": 167539.0,
                                "worst_system_scnid": 1475
                            }
                        ],
                        "stress_loss_over_margin": 167471.0,
                        "stress_value_liquidity_risk": -121.0,
                        "stress_value_market_risk": 53.0,
                        "total_margin_requirement": 167539.0
                    },
                    {
                        "liquidation_group": 'null',
                        "margin_group_code": "!DB10",
                        "slom_per_lgs_mc": [
                            {
                                "liquidation_group_split": 'null',
                                "margin_class_code": "DB10",
                                "stress_loss_over_margin": -101976005.0,
                                "stress_value_liquidity_risk": -1310.0,
                                "stress_value_market_risk": -107168880.0,
                                "total_margin_requirement": 5194185.0,
                                "worst_system_scnid": 449
                            }
                        ],
                        "stress_loss_over_margin": -101976005.0,
                        "stress_value_liquidity_risk": -1310.0,
                        "stress_value_market_risk": -107168880.0,
                        "total_margin_requirement": 5194185.0
                    }
                ],
                "stress_loss_over_margin": -101808201.0,
                "stress_value": -107168880.0,
                "total_margin_requirement": 5362113.0
            }
        ],
        "stress_loss_over_margin": -101808201.0,
        "worst_global_scenario": "Lehman crash 15.09.2008"
    },
    "errors": [
        {
            "error_msg": "Line 1 instrument iid not recognized: 736947",
            "line_no": 2,
            "portfolio": "ETD"
        }
    ],
    "etd_positions": [
        {
            "call_put_flag": "C",
            "contract_date": 20311222,
            "exercise_price": 90,
            "iid": 18249016,
            "line_no": 1,
            "liquidation_group": "PEQ01",
            "liquidation_group_split": "PEQ01_HP3",
            "maturity": 203112,
            "net_ls_balance": 10,
            "product_id": "OEXD",
            "stress_value_per_global_scenario": [
                {
                    "gscnid": 1,
                    "stress_value": 53.0
                }
            ],
            "version_number": "0"
        }
    ],
    "live": 'false',
    "live_timestamp": 0,
    "portfolio_margin": [
        {
            "initial_margin": 3161.708587,
            "liquidation_group": "PEQ01",
            "liquidation_group_split": "PFI01_HP2_T0-99999",
            "liquidity_addon": 6.442439,
            "long_option_credit": 0,
            "market_risk": 3155.266149,
            "market_risk_per_rms": [
                {
                    "rms_components": [
                        {
                            "compression_adjustment": 10,
                            "correlation_break_adjustment": 500,
                            "risk_measure_value": 4481.692879,
                            "subsample_id": 1
                        }
                    ],
                    "rms_market_risk": 4991.692879,
                    "rms_name": "FILTERED_HISTORICAL_VAR_2",
                    "simulation_type": "Historical",
                    "weighting_factor": 0.51
                }
            ],
            "premium_margin": 0,
            "time_to_expiry_adjustment": 0
        }
    ],
    "rbm_margin": {
        "margin_classes": [
            {
                "additional_margin": 1026812,
                "additional_margin_before_grouping": 1026812,
                "cash_interest_rate": -0.566,
                "current_liquidating_margin": 851977,
                "margin_class_code": "DB10",
                "margin_class_currency": "EUR",
                "margin_group_code": 'null',
                "margin_parameter": 5.5,
                "margin_parameter_flag": "P",
                "positions": [
                    {
                        "amount_clv_cash": -10310484,
                        "amount_clv_secu": 62100,
                        "current_liquidating_margin": 851977,
                        "line_no": 1,
                        "net_cash_position": -10310484,
                        "net_security_position": 64100,
                        "sec_isin": "DE0005810055",
                        "sec_name": "DEUTSCHE BOERSE AG",
                        "settlement_date": 20210312
                    }
                ]
            }
        ]
    }
}

global_scenarios_200 = {
    "business_date": 20220912,
    "live": 'false',
    "live_timestamp": 0,
    "scenarios": [
        {
            "global_scenario": "Lehman crash 15.09.2008",
            "gscnid": 1
        }
    ]
}

stress_test = {
    "portfolio_components": [
        {
            "etd_portfolio": [
                {
                    "contract_date": 20301220,
                    "line_no": 1,
                    "net_ls_balance": 1,
                    "product_id": "FEXD"
                }
            ],
            "type": "etd_portfolio"
        },
        {
            "cash_csv": {
                "csv": "Security ISIN,Settlement Date,Settlement Currency,Payable Cash Amount,Traded Price,Security Quantity,CCP Trade Number,Leg Type\\nDE0005810055,20220630,,,150.75,100,,\\nDE000A1684V3,20220630,,,99.3,100,,"
            },
            "type": "cash_csv"
        }
    ]
}

stress_test_200 = {
    "business_date": 20220905,
    "cash_stress_test_liqu_summary": [
        {
            "currency": "EUR",
            "margin_class": "DB10",
            "scenario": [
                {
                    "diff2current": 0,
                    "liqu_value_eur": -1660.0797781885303,
                    "liqu_value_sum": -1660.0797781885303,
                    "scenario_id": "-"
                }
            ]
        }
    ],
    "cash_stress_test_liqu_value": [
        {
            "coupon_adjustment": 0,
            "currency": "EUR",
            "fx_rate": 1,
            "line_no": "2",
            "margin_class": "DB10",
            "net_cash_position": -15075,
            "net_security_position": 100,
            "price_unit": "A",
            "scenario": [
                {
                    "diff2current": 0,
                    "discounting_factor": 1.0000047671460133,
                    "interest_rate": -0.087,
                    "liqu_value": -1660.0797781885303,
                    "liqu_value_cash": 15075,
                    "liqu_value_eur": -1660.0797781885303,
                    "liqu_value_secu": -16735.07977818853,
                    "price": 167.35,
                    "price_offset": 0,
                    "price_offset_type": "A",
                    "projected_price": 167.35,
                    "rh_interest_rate": 0.913,
                    "rl_interest_rate": -1.087,
                    "scenario_id": "-"
                }
            ],
            "sec_isin": "DE0005810055",
            "security_type": "S",
            "settlement_currency": "EUR",
            "settlement_date": 20220630
        }
    ],
    "errors": [
        {
            "error_msg": "Line 1 instrument iid not recognized: 736947",
            "line_no": 2,
            "portfolio": "ETD"
        }
    ],
    "live": 'false',
    "live_timestamp": 0,
    "position_stress_test": [
        {
            "call_put": "",
            "contract_date": 20301220,
            "contract_month": 12,
            "contract_year": 2030,
            "exercise_price": 0,
            "expiry_day": 0,
            "flex_contract_symbol": "",
            "iid": 42741021,
            "line_no": "1",
            "liquidation_group": "PEQ01",
            "liquidation_group_split": "PEQ01_HP3",
            "net_quantity_ea": 0,
            "net_quantity_ls": 1,
            "neutral_price": 90.14623999999999,
            "product": "FEXD",
            "stress_value": [
                {
                    "scnid": 1477,
                    "stress_pnl": {
                        "amount": 446.37538928000043,
                        "currency": "USD"
                    },
                    "stress_pnl_product_currency": {
                        "amount": 449.6126000000004,
                        "currency": "EUR"
                    },
                    "stress_scenario_price": 95.296126,
                    "stress_value": {
                        "amount": 446.37538928000043,
                        "currency": "USD"
                    },
                    "stress_value_product_currency": {
                        "amount": 449.6126000000004,
                        "currency": "EUR"
                    },
                    "system_scn_code": "HIST_PEQ01_CMM_2001",
                    "system_scn_purpose": "Clearing Fund Historical",
                    "system_scn_text": "Capital Market Move 06.12.2001"
                }
            ],
            "version": "0"
        }
    ]
}