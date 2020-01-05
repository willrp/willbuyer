//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState } from "react";
import { Icon, Button } from "semantic-ui-react";
import { DateRangePicker } from "react-dates";

//IMPORT HOOKS==============================================================
import useIsPhone from "hooks/is-phone";

//COMPONENT=================================================================
function DateRange({ initialRange, onDatesChange }) {
    const [showClearDates, setShowClearDates] = useState((initialRange.startDate !== null && initialRange.endDate !== null));
    const [dateRange, setDateRange] = useState(initialRange);
    const [focusedInput, setfocusedInput] = useState(null);

    const isPhone = useIsPhone();

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
                    readOnly={true}
                    displayFormat="YYYY/MM/DD"
                    isOutsideRange={() => false}
                    hideKeyboardShortcutsPanel={true}
                    numberOfMonths={(isPhone) ? 1 : 2}
                    withFullScreenPortal={isPhone}
                    disableScroll={isPhone}
                    small={true}
                />
                {showClearDates && <Button icon circular className="DateRangePickerClear_button" onClick={clearDates}><Icon name="x" /></Button>}
            </Fragment>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default DateRange;