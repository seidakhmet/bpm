Ext.onReady(function () {
            Ext.application({
                name: '{% trans "Business processes" %}',

                launch: function () {
                    let store = Ext.create('Ext.data.Store', {
                        fields: [
                            "id",
                            "title",
                            "excel_file",
                            "status",
                            "deadline",
                            "min_bpm_group",
                            "creator_full_name",
                        ],
                        proxy: {
                            type: 'ajax',
                            url: '/api/v1/tasks/business-process/',
                            reader: {
                                type: 'json',
                                rootProperty: 'data'
                            }
                        },
                        autoLoad: true
                    });


                    let grid = Ext.create({
                        xtype: 'grid',
                        title: "Business processes",
                        layout: 'fit',
                        fullscreen: true,
                        columns: [
                            {
                                text: "ID",
                                dataIndex: "id",
                                flex: 1,
                            },
                            {
                                text: "{% trans 'Title' %}",
                                dataIndex: "title",
                                flex: 1,
                                editor: {
                                    xtype: 'textfield',
                                    allowBlank: false
                                }
                            },
                            {
                                text: "{% trans 'Status' %}",
                                dataIndex: "status",
                                flex: 1,
                            },
                            {
                                text: "{% trans 'Deadline' %}",
                                dataIndex: "deadline",
                                flex: 1,
                            },
                            {
                                text: "{% trans 'Minimal BPM group' %}",
                                dataIndex: "min_bpm_group",
                                flex: 1,
                            },
                            {
                                text: "{% trans 'Creator' %}",
                                dataIndex: "creator_full_name",
                                flex: 1,
                            },
                            {
                                text: 'Actions',
                                flex: 1,
                                renderer: function (value, metaData, record) {
                                    return '<button>Edit</button>' +
                                        '<button>Delete</button>';
                                }
                            }
                        ],
                        store: store,
                        plugins: {
                            gridcellediting: {
                                selectOnEdit: true
                            },
                            rowoperations: {
                                operation: {
                                    text: 'Archive',
                                    handler: function (grid, rowIndex, colIndex) {
                                        let rec = grid.getStore().getAt(rowIndex);
                                        Ext.Msg.alert('Archive', rec.get('title'));
                                    },
                                    ui: 'alt'
                                }
                            }
                        }
                    });

                }
            });
        });