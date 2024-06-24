# This Dataset isn't suitable for evaluation
Data format is messy with alot of json files without json formatting, there are input data with "/n" and also "//n".
With the function I constructed, the answer rates are shown as below:
| Dataset | Score              | IO Errors |
| ------- | ------------------ | ------ |
| dev     | 12.5 / 18              | 82     |
| train   | 14.666666666666666 /16 | 84     |
| test    | 9.833333333333332 / 14 | 86     |
(I used the answers from the `Accepted.json` and also mark timeouts as IO errors)