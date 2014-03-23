import unittest
import time
import master_common


DEFAULT_BRANCH_PRIORITY = master_common.DEFAULT_BRANCH_PRIORITY
BRANCH_PRIORITIES = master_common.BRANCH_PRIORITIES


class builderStatusStub(object):
    def __init__(self, category):
        self.category = category


def builderPrioriesStub(branch):
    properties = {}
    properties['branch'] = branch
    return properties


class builderStub(object):
    def __init__(self, name, branch, category):
        self.properties = builderPrioriesStub(branch)
        self.name = name
        self.category = category
        self.builder_status = builderStatusStub(category)

    def get_priority_request(self, request):
        return master_common.builderPriority(self, request)


class Request(object):
    def __init__(self, priority, submitted_at):
        self.priority = priority
        self.submitted_at = submitted_at

    def get_request(self):
        return (None, self.priority, self.submitted_at)


def requestStub(priority, submitted_at):
    return (None, priority, submitted_at)


class builderProrityTest(unittest.TestCase):

    def setUp(self):
        # low priority branches:
        # generic builder, oak, release
        self.oak_release = builderStub(name='oak builder',
                                       branch='oak',
                                       category='release')
        # generic builder, oak, non release
        self.oak_builder = builderStub(name='oak release',
                                       branch='oak',
                                       category='non-release')
        # high priority branches:
        # generic builder, mozilla-release, release
        self.mr_release = builderStub(name='release job',
                                      branch='mozilla-release',
                                      category='release')

        # generic builder, mozilla-release, non release
        self.mr_builder = builderStub(name='generic release job',
                                      branch='mozilla-release',
                                      category='non-release')

        # l10n stuff... very low priority
        self.l10n_release = builderStub(name='l10n',
                                        branch='oak',
                                        category='release')
        self.l10n_builder = builderStub(name='l10n',
                                        branch='oak',
                                        category='non-release')

        # requests
        submitted_at = int(time.time())
        last_hour = submitted_at - 3600
        last_day = submitted_at - (3600 * 24)
        last_week = submitted_at - (3600 * 24 * 7)

        self.high_priority_request = requestStub(1, submitted_at)
        self.low_priority_request = requestStub(5, submitted_at)

        self.one_hour_old_hp_request = requestStub(1, last_hour)
        self.one_hour_old_hp_request = requestStub(5, last_hour)

        self.one_day_old_hp_request = requestStub(1, last_day)
        self.one_day_old_lp_request = requestStub(5, last_day)

        self.one_week_old_hp_request = requestStub(1, last_week)
        self.one_week_old_lp_request = requestStub(5, last_week)

    def test_release(self):
        oak_builder = self.oak_builder
        oak_release = self.oak_release

        request = self.high_priority_request

        # same request, different builders
        p0 = oak_release.get_priority_request(request)
        p1 = oak_builder.get_priority_request(request)
        self.assertTrue(p0 < p1)

    def test_branch_priority(self):
        oak_builder = self.oak_builder
        l10n_builder = self.l10n_builder

        # request
        request = self.low_priority_request

        p0 = oak_builder.get_priority_request(request)
        p1 = l10n_builder.get_priority_request(request)
        self.assertTrue(p0 < p1)

    def test_timestamp_priority(self):
        oak_builder = self.oak_builder
        request_1 = self.low_priority_request
        request_2 = self.one_hour_old_hp_request

        p0 = oak_builder.get_priority_request(request_2)
        p1 = oak_builder.get_priority_request(request_1)
        self.assertTrue(p0 < p1)

    def test_request_priority(self):
        oak_builder = self.oak_builder

        low_priority_request = self.low_priority_request
        high_priority_request = self.high_priority_request

        p0 = oak_builder.get_priority_request(high_priority_request)
        p1 = oak_builder.get_priority_request(low_priority_request)
        self.assertTrue(p0 < p1)

    def test_release_priority(self):
        mr_release = self.mr_release
        oak_builder = self.mr_release

        low_priority_request = self.low_priority_request
        p0 = mr_release.get_priority_request(low_priority_request)
        p1 = oak_builder.get_priority_request(low_priority_request)
        print
        print p0
        print p1
        print
        self.assertTrue(p0 < p1)

        # now increase oak_builder priority
        high_priority_request = self.high_priority_request
        p1 = oak_builder.get_priority_request(high_priority_request)
        self.assertTrue(p0 < p1)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
