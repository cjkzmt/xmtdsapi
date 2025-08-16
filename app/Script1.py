    rows = await Data.filter(
    Script_id__in=[s.id for s in Scripts],
    Account__status='ENABLE'
        ).values(
            'id', 'Script_id', 'Account_id',
            'Account__Platform__name',
            'Account__Platform__publishurl',
            'Account__Platform__character',
            'Account__Platform__keycount',
            'Account__Platform__verification',
            'Account__Platform__advance',
            'Account__Platform__publishverif',
            'status')