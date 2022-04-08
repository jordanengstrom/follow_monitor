# twarc2 following 789276634389950464 results.jsonl
test_data = [{
    "data": [
        {
            "id": "6253282",
            "name": "Twitter API",
            "username": "TwitterAPI"
        },
        {
            "id": "2244994945",
            "name": "Twitter Dev",
            "username": "TwitterDev"
        },
        {
            "id": "783214",
            "name": "Twitter",
            "username": "Twitter"
        },
        {
            "id": "95731075",
            "name": "Twitter Safety",
            "username": "TwitterSafety"
        },
        {
            "id": "3260518932",
            "name": "Twitter Moments",
            "username": "TwitterMoments"
        },
        {
            "id": "373471064",
            "name": "Twitter Music",
            "username": "TwitterMusic"
        },
        {
            "id": "791978718",
            "name": "Twitter Official Partner",
            "username": "OfficialPartner"
        },
        {
            "id": "17874544",
            "name": "Twitter Support",
            "username": "TwitterSupport"
        },
        {
            "id": "234489024",
            "name": "Twitter Comms",
            "username": "TwitterComms"
        },
        {
            "id": "1526228120",
            "name": "Twitter Data",
            "username": "TwitterData"
        }
    ],
    "meta": {
        "result_count": 10,
        "next_token": "DFEDBNRFT3MHCZZZ"
    }
},
    {
        "data": [
            {
                "id": "6253282",
                "name": "Twitter API",
                "username": "TwitterAPI"
            },
            {
                "id": "2244994945",
                "name": "Twitter Dev",
                "username": "TwitterDev"
            },
            {
                "id": "783214",
                "name": "Twitter",
                "username": "Twitter"
            },
            {
                "id": "95731075",
                "name": "Twitter Safety",
                "username": "TwitterSafety"
            },
            {
                "id": "3260518932",
                "name": "Twitter Moments",
                "username": "TwitterMoments"
            },
            {
                "id": "373471064",
                "name": "Twitter Music",
                "username": "TwitterMusic"
            },
            {
                "id": "791978718",
                "name": "Twitter Official Partner",
                "username": "OfficialPartner"
            },
            {
                "id": "17874544",
                "name": "Twitter Support",
                "username": "TwitterSupport"
            },
            {
                "id": "234489024",
                "name": "Twitter Comms",
                "username": "TwitterComms"
            },
            {
                "id": "1526228120",
                "name": "Twitter Data",
                "username": "TwitterData"
            }
        ],
        "meta": {
            "result_count": 10,
            "next_token": "9232DFT3MHCZZZ"
        }
    },
    {
        "data": [
            {
                "id": "6253282",
                "name": "Twitter API",
                "username": "TwitterAPI"
            },
            {
                "id": "2244994945",
                "name": "Twitter Dev",
                "username": "TwitterDev"
            },
            {
                "id": "783214",
                "name": "Twitter",
                "username": "Twitter"
            },
            {
                "id": "95731075",
                "name": "Twitter Safety",
                "username": "TwitterSafety"
            },
            {
                "id": "3260518932",
                "name": "Twitter Moments",
                "username": "TwitterMoments"
            },
            {
                "id": "373471064",
                "name": "Twitter Music",
                "username": "TwitterMusic"
            },
            {
                "id": "791978718",
                "name": "Twitter Official Partner",
                "username": "OfficialPartner"
            },
            {
                "id": "17874544",
                "name": "Twitter Support",
                "username": "TwitterSupport"
            },
            {
                "id": "234489024",
                "name": "Twitter Comms",
                "username": "TwitterComms"
            },
            {
                "id": "1526228120",
                "name": "Twitter Data",
                "username": "TwitterData"
            }
        ],
        "meta": {
            "result_count": 10,
        }
    },
]

test_arr = []
i = 0
next_token = test_data[i]['meta']['next_token']

while next_token is not None:
    test_arr.extend(test_data[i]['data'])

    i += 1
    next_request = test_data[i]
    if 'meta' in next_request.keys():
        if 'next_token' in next_request['meta'].keys():
            next_token = next_request['meta']['next_token']
        else:
            next_token = None
            test_arr.extend(test_data[i]['data'])
            break

print('we made it')
print(f'len people_i_follow: {len(test_arr)}')
