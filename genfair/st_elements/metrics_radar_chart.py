from typing import Optional

from streamlit_elements import elements, mui, html


def metrics_radar_chart(scores: dict, key: Optional[str] = None):

    with elements(key=key): # type: ignore

        from streamlit_elements import nivo
        
        DATA = [
            { "dimension": "SAM", "score": scores.get("SAM", 0), },
            { "dimension": "GPD", "score": scores.get("GPD", 0), },
            { "dimension": "SCS", "score": scores.get("SCS", 0), },
            { "dimension": "ORR", "score": scores.get("ORR", 0), },
            { "dimension": "CRA", "score": scores.get("CRA", 0), },
        ]

        with mui.Box(sx={"height": 500}):
            nivo.Radar(
                data=DATA,
                keys=["score"],
                indexBy="dimension",
                valueFormat=">-.2f",
                maxValue=5,
                margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                borderColor={ "from": "color" },
                gridLabelOffset=36,
                dotSize=10,
                dotColor={ "theme": "background" },
                dotBorderWidth=2,
                motionConfig="wobbly",
                legends=[
                    {
                        "anchor": "top-left",
                        "direction": "column",
                        "translateX": -50,
                        "translateY": -40,
                        "itemWidth": 80,
                        "itemHeight": 20,
                        "itemTextColor": "#999",
                        "symbolSize": 12,
                        "symbolShape": "circle",
                        "effects": [
                            {
                                "on": "hover",
                                "style": {
                                    "itemTextColor": "#000"
                                }
                            }
                        ]
                    }
                ],
                theme={
                    "background": "#FFFFFF",
                    "textColor": "#31333F",
                    "tooltip": {
                        "container": {
                            "background": "#FFFFFF",
                            "color": "#31333F",
                        }
                    }
                }
            )
            