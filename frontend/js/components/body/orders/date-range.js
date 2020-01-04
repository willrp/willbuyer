//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState } from "react";
import { Icon, Button } from "semantic-ui-react";
import { DateRangePicker } from "react-dates";

//COMPONENT=================================================================
function DateRange({ onDatesChange }) {
    const [showClearDates, setShowClearDates] = useState(false);
    const [dateRange, setDateRange] = useState({startDate: null, endDate: null});
    const [focusedInput, setfocusedInput] = useState(null);

    function clearDates() {
        setShowClearDates(false);
        setDateRange({ startDate: null, endDate: null });
        onDatesChange({ startDate: null, endDate: null });
    }

    function changeDates({ startDate, endDate }) {
        setShowClearDates(true);
        setDateRange({ startDate, endDate });
        if(startDate !== null && endDate !== null) {
            onDatesChange({ startDate, endDate });
        }
    }

    function render() {
        const { startDate, endDate } = dateRange;
        return (
            <Fragment>
                <DateRangePicker
                    startDate={startDate}
                    startDateId="DATE_START"
                    endDate={endDate}
                    endDateId="DATE_END"
                    onDatesChange={changeDates}
                    focusedInput={focusedInput}
                    onFocusChange={(input) => setfocusedInput(input)}
                    noBorder={true}
                    displayFormat="YYYY/MM/DD"
                    isOutsideRange={() => false}
                    hideKeyboardShortcutsPanel={true}
                    customArrowIcon={<Icon name="arrow alternate circle right outline" size="big" />}
                />
                {showClearDates && <Button icon circular className="DateRangePickerClear_button" onClick={clearDates}><Icon name="x" /></Button>}
            </Fragment>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default DateRange;