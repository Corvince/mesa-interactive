import solara
import altair as alt
import pandas as pd


def make_chart(variables, title):
    @solara.component
    def Chart(model):
        initial_data = {"Step": [0]}
        for var in variables:
            initial_data[var] = [getattr(model, var, None)]

        data, set_data = solara.use_state(pd.DataFrame(initial_data))

        def update_data():
            new_row = {"Step": model.schedule.steps}
            for var in variables:
                new_row[var] = getattr(model, var, None)

            new_data = pd.DataFrame([new_row])

            # Drop any existing rows that are past the current step
            filtered_data = data[data["Step"] < model.schedule.steps]

            # Concatenate the filtered old data with the new data
            set_data(pd.concat([filtered_data, new_data]))

        solara.use_memo(update_data, dependencies=[model])

        chart = (
            alt.Chart(data.melt("Step"))
            .mark_line()
            .encode(
                alt.X("Step", axis=alt.Axis(tickMinStep=1, tickCount=len(data))),
                y="value",
                color="variable",
            )
        )

        chart = chart.properties(title=title)
        return solara.FigureAltair(chart)

    return Chart
