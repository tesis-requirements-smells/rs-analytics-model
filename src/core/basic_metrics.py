class BasicMetrics:


    def evaluate_metric(self, metric_id, params):
        if metric_id == 'PRRC':
            return self._evaluate_PRRC(params)
        elif metric_id == 'PRRDE':
            return self._evaluate_PRRDE(params)
        elif metric_id == 'PRPND':
            return self._evaluate_PRPND(params)
        elif metric_id == 'PRNAON':
            return self._evaluate_PRNAON(params)
        elif metric_id == 'NSEHU':
            return self._evaluate_NSEHU(params)
        elif metric_id == 'PTCR':
            return self._evaluate_PTCR(params)
        elif metric_id == 'RECR':
            return self._evaluate_RECR(params)
        elif metric_id == 'PTAR':
            return self._evaluate_PTAR(params)
        else:
            print(f'La métrica { metric_id } no es válida')
            return None
        


    def _evaluate_PRRC(self, params):
        NRRC = int(params['NRRC'])
        NTR = int(params['NTR'])

        return (int(NRRC) / int(NTR)) * 100
    

    def _evaluate_PRRDE(self, params):
        NRRDE = int(params['NRRDE'])
        NTR = int(params['NTR'])

        return (int(NRRDE) / int(NTR)) * 100
    

    def _evaluate_PRPND(self, params):
        NRPND = int(params['NRPND'])
        NTR = int(params['NTR'])

        return (int(NRPND) / int(NTR)) * 100    


    def _evaluate_PRNAON(self, params):
        NRNAON = int(params['NRNAON'])
        NTR = int(params['NTR'])

        return (int(NRNAON) / int(NTR)) * 100
    

    def _evaluate_NSEHU(self, params):
        NSEHU = int(params['NSEHU'])

        return int(NSEHU)
    

    def _evaluate_PTCR(self, params):
        TTCR = int(params['TTCR'])
        NTR = int(params['NTR'])

        return int(TTCR) / int(NTR)
    

    def _evaluate_RECR(self, params):
        ERCR = int(params['ERCR'])
        EECR = int(params['EECR'])

        return int(ERCR) / int(EECR)
    

    def _evaluate_PTAR(self, params):
        TTAR = int(params['TTAR'])
        NTR = int(params['NTR'])

        return int(TTAR) / int(NTR)




    