"""
Single page performance tests for LMS.
"""
from bok_choy.web_app_test import WebAppTest, with_cache
from ..pages.lms.auto_auth import AutoAuthPage
from ..pages.lms.courseware import CoursewarePage
from ..pages.lms.dashboard import DashboardPage
from nose.plugins.attrib import attr

@attr(har_mode='explicit')
class LMSPagePerformanceTest(WebAppTest):
    """
    Base class to capture LMS performance with HTTP Archives.

    To import courses for the bok choy tests, pass the --imports_dir=<course directory> argument to the paver command
    where <course directory> contains the (un-archived) courses to be imported.
    """
    course_org = 'edX'
    course_num = 'Open_DemoX'
    course_run = 'edx_demo_course'

    def setUp(self):
        """
        Authenticate as staff so we can view and edit courses.
        """
        super(LMSPagePerformanceTest, self).setUp()
        AutoAuthPage(self.browser).visit()

    def record_visit_coursware(self):
        """
        Produce a HAR for loading the Coursware page.
        """
        courseware_page = CoursewarePage(self.browser, self.course_id)
        har_name = 'CoursewarePage_{org}_{course}'.format(
            org=self.course_org,
            course=self.course_num
        )
        self.har_capturer.add_page(self.browser, har_name)
        courseware_page.visit()
        self.har_capturer.save_har(self.browser, har_name)

    def record_visit_dashboard(self):
        """
        Produce a HAR for loading the Dashboard page.
        """
        dashboard_page = DashboardPage(self.browser, self.course_id)
        har_name = 'DashboardPage{org}_{course}'.format(
            org=self.course_org,
            course=self.course_num
        )
        self.har_capturer.add_page(self.browser, har_name)
        dashboard_page.visit()
        self.har_capturer.save_har(self.browser, har_name)


class LmsDemoPerformanceTest(LMSPagePerformanceTest):
    """
    Test LMS performance on the Open_DemoX course.
    """

    @with_cache
    def test_visit_coursware(self):
        """
        Record visiting the Justice Coursware page.
        """
        self.record_visit_coursware()

    @with_cache
    def test_visit_dashboard(self):
        """
        Record visiting a Justice Dashboard page
        """
        self.record_visit_dashboard()
