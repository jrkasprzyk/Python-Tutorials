import pandas as pd #for dataframes and data processing
import numpy as np #for numerical computation
import sys #system functions

def convert_cms_to_mcm(val):
  return val*24*60*60/1e6

def storage_to_elevation(sto, rating_df):
  sto_lookup = rating_df["Storage"].to_numpy()
  elev_lookup = rating_df["Elevation"].to_numpy()
  return np.interp(sto, sto_lookup, elev_lookup)

def elevation_to_storage(elev, rating_df):
  sto_lookup = rating_df["Storage"].to_numpy()
  elev_lookup = rating_df["Elevation"].to_numpy()
  return np.interp(elev, elev_lookup, sto_lookup)

def res_sim_with_elev(timeseries_df, rule_curve, initial_storage, storage_capacity):
    # input:assume a df with Inflow and Demand for the entire timeseries,
    # in volume units.
    #
    # the initial_storage is assumed to occur before the timeseries begins,
    # in same units as other volume variables
    #
    # the storage_capacity is assumed to be exact (anything over this value
    # will spill)
    #
    # output: this function will populate Storage, Delivery, Spill, Outflow

    # Assumptions: assume reservoir can release all storage to meet demand
    # spill occurs if storage exceeds capacity
    # no capacity constraints for releasing spill

    # process timeseries information
    inflow = timeseries_df['Inflow'].to_numpy()
    demand = timeseries_df['Demand'].to_numpy()
    N = len(inflow)
    storage_vol = np.zeros(N)
    storage_elev = np.zeros(N)
    delivery = np.zeros(N)
    spill = np.zeros(N)
    outflow = np.zeros(N)

    storage_vol[0] = initial_storage
    storage_elev[0] = storage_to_elevation(initial_storage)

    for i in range(N):
        # assume the inflow and the current storage volume at the current timestep
        # is all available to meet demand
        available_water = inflow[i] + storage_vol[i]

        # priority 1: meet all demand
        if available_water > demand[i]:
            # deliver all the water that is requested
            meets_demand = True
            trial_storage = storage_vol[i] + inflow[i] - demand[i]
        else:
            # demand is higher than supply, so we would be inclined to
            # release all that we have
            meets_demand = False
            trial_storage = 0.0

        # priority 2: flood control
        trial_elev = storage_to_elevation(trial_storage)

        if trial_elev >= rule_curve['Top']:
            #emergency operations
        else if trial_elev >= rule_curve['Flood Start']:
            # release all of trial storage plus more
        else if trial_elev >= rule_curve['Conservation Start']:
            # regular releases
        else if trial_elev < rule_curve['Conservation Start']:
            # dead storage

        # check storage capacity, and update storage unless you're at the end of the
        # simulation
        if trial_storage > storage_capacity:
            spill[i] = trial_storage - storage_capacity
            if i < N - 1:
                storage_vol[i + 1] = storage_capacity
        else:
            spill[i] = 0
            if i < N - 1:
                storage_vol[i + 1] = trial_storage

        # store outflow as the sum of both spill and delivery
        outflow[i] = spill[i] + delivery[i]

    # before exiting, save the data into the dataframe, which is the only thing
    # returned
    timeseries_df['Storage'] = storage_vol
    timeseries_df['Delivery'] = delivery
    timeseries_df['Spill'] = spill
    timeseries_df['Outflow'] = outflow

    return timeseries_df

def transition_from_to_full(sto, cap):

  # input: sto is a numpy array of the storage record
  # so for example you can call the below outside this function:
  # daily_df["Storage"].to_numpy()

  # and cap is the capacity that is considered full

  # to do the calculation,
  # save an array that will be 'true' if the timestep's storage is less than
  # capacity. We add a 0 to the beginning of the end so we can handle transitions
  # for the beginning and end of the period

  is_less_than_full = np.append([0], sto < cap)
  is_less_than_full = np.append(is_less_than_full, [0])

  # here, at each timestep we note situations in which there's a change
  # in the timestep between being full previously and now less than full
  # and to process this, we want there to be 1 and 0 instead of True and False
  # (this is accomplished by the .astype(int) call)

  change_from_full = np.diff(is_less_than_full.astype(int))

  # uncomment the below to visualize:
  #np.set_printoptions(threshold=sys.maxsize)
  #print(change_from_full)

  # change_from_full will show a 1 when the series goes
  # from full to less than full, and a -1 when the series
  # goes from being less than full to full again. This is the
  # "event" we care about.

  # below, we keep track of all of the entries in which
  # we find a 1 (signalling that draining is beginning)
  # and a -1 (signalling that the reservoir is full again)
  start = np.flatnonzero(change_from_full == 1)
  end = np.flatnonzero(change_from_full == -1)

  # now for each event we will know the indexes where it started and ended
  # (calculated above) as well as the length:
  length = end - start

  df = pd.DataFrame()
  df['Start'] = start
  df['End'] = end
  df['Length'] = length

  return df

# make sure the Excel file is uploaded to your directory
daily_df = pd.read_excel('Des_Moines_River_flow.xls', index_col=0)

daily_df['Inflow'] = convert_cms_to_mcm(daily_df['Average flow (m3/s)'].to_numpy())

daily_df['Demand'] = 2.5

daily_df = reservoir_simulation(daily_df, 750, 750)
daily_df['Storage'].plot()

storage = daily_df["Storage"].to_numpy()

events_df = transition_from_to_full(storage, 750)

# we call the "critical period" the time period that was the longest
# to go from the reservoir being completely full, to empty, to full again
# (i.e., the longest "length" in all the events we just found)
crit_period_length = np.max(events_df["Length"].to_numpy())

# of all the events we stored, which one constitutes the longest one?
crit_period_eventindex = np.argmax(events_df["Length"].to_numpy())

# iloc allows us to pull out a row of a dataframe, with the index we just found.
# it's a convenient way to display the information we need -- the start day, the end
# day, and the length of the event.
events_df.iloc[crit_period_eventindex]

# in this command, we are storing a new daily dataframe that only constitutes
# the rows that fall between a start and an end day.
worst_event_df = daily_df.iloc[600:3000]

# plot all the columns
worst_event_df.plot()

